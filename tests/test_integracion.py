"""Regresiones de la integración de Ismael y Carlos, sin escribir en el log real."""

import io
import tempfile
import unittest
from contextlib import redirect_stdout
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

import auditoria
import main
from grafo_red import GrafoRed
from servidor import Servidor
from tabla_hash import TablaHash


class PruebasIntegracion(unittest.TestCase):
    # Aísla la configuración global de auditoría y la restaura después de cada prueba.
    def setUp(self):
        self.addCleanup(
            auditoria.configurar_auditoria,
            auditoria._auditoria_activa,
            auditoria._ruta_archivo,
        )
        auditoria.configurar_auditoria(False)

    # Devuelve un log temporal y activa auditoría solo sobre ese archivo de prueba.
    def preparar_log(self):
        carpeta = tempfile.TemporaryDirectory(prefix="network_os_test_")
        self.addCleanup(carpeta.cleanup)
        ruta = Path(carpeta.name) / "auditoria.txt"
        auditoria.configurar_auditoria(True, ruta)
        return ruta

    # Las entradas no finitas se rechazan sin insertar enlaces ni registrar eventos.
    def test_latencias_invalidas_no_modifican_red(self):
        red = GrafoRed()
        red.agregar_servidor(Servidor("A"))
        red.agregar_servidor(Servidor("B"))

        for latencia in (float("nan"), float("inf"), -float("inf"), 0, -5):
            with self.subTest(latencia=latencia):
                with patch("grafo_red.registrar_evento") as registrar:
                    with self.assertRaises(ValueError):
                        red.agregar_conexion("A", "B", latencia)
                    registrar.assert_not_called()
                self.assertEqual(red.adyacencias, [[], []])

        red.agregar_conexion("A", "B", 2.5)
        self.assertEqual(red.adyacencias, [[(1, 2.5)], [(0, 2.5)]])

    # Verifica la fórmula de Carlos y que el encadenamiento mantiene usuarios distintos.
    def test_hash_orden_colisiones_y_autenticacion(self):
        tabla = TablaHash()
        self.assertEqual([tabla.funcion_hash(n) for n in ("ana", "naa", "aan")], [0, 6, 2])
        self.assertEqual(tabla.funcion_hash("a"), tabla.funcion_hash("k"))
        self.assertTrue(tabla.registrar_usuario("a", "clave_a"))
        self.assertTrue(tabla.registrar_usuario("k", "clave_k"))
        self.assertFalse(tabla.registrar_usuario("a", "otra"))
        self.assertTrue(tabla.autenticar("a", "clave_a"))
        self.assertTrue(tabla.autenticar("k", "clave_k"))
        self.assertFalse(tabla.autenticar("a", "clave_k"))
        self.assertFalse(tabla.autenticar("inexistente", "clave_a"))

    # Comprueba append sin salto final previo, UTF-8 y ~ dentro de la descripción.
    def test_auditoria_conserva_historial_y_separadores(self):
        ruta = self.preparar_log()
        anterior = "servidor~evento anterior~01:10:2026 10:00:00~"
        ruta.write_text(anterior, encoding="utf-8")
        self.assertTrue(auditoria.registrar_evento("autenticación", "usuario Ana~María"))
        self.assertTrue(auditoria.registrar_evento("red", "conexión agregada"))

        contenido = ruta.read_text(encoding="utf-8")
        self.assertTrue(contenido.startswith(anterior + "\n"))
        registros = auditoria.obtenerRegistros()
        self.assertEqual(len(registros), 3)
        self.assertEqual(registros[1][1], "usuario Ana~María")
        self.assertEqual(registros[2][1], "conexión agregada")

    # Omite una línea incompleta y una fecha inválida, sin perder el registro válido.
    def test_auditoria_omite_lineas_invalidas(self):
        ruta = self.preparar_log()
        ruta.write_text(
            "linea incompleta\nmodulo~accion~fecha incorrecta~\n",
            encoding="utf-8",
        )
        auditoria.registrar_evento("red", "evento válido")
        salida = io.StringIO()
        with redirect_stdout(salida):
            registros = auditoria.obtenerRegistros()
        self.assertEqual(len(registros), 1)
        self.assertEqual(registros[0][1], "evento válido")
        self.assertIn("línea 1", salida.getvalue())
        self.assertIn("línea 2", salida.getvalue())

    # Los filtros incluyen el día solicitado y respetan los límites entre fechas.
    def test_filtros_de_auditoria(self):
        self.preparar_log()
        with patch("auditoria.datetime", wraps=datetime) as reloj:
            for dia in (6, 7, 8):
                reloj.now.return_value = datetime(2026, 10, dia, 12, 0)
                auditoria.registrar_evento("prueba", f"evento_dia_{dia}")

        salida = io.StringIO()
        with redirect_stdout(salida):
            self.assertTrue(auditoria.leerRegistroFecha("07:10:2026"))
        self.assertIn("evento_dia_7", salida.getvalue())
        self.assertNotIn("evento_dia_6", salida.getvalue())
        self.assertNotIn("evento_dia_8", salida.getvalue())

        salida = io.StringIO()
        with redirect_stdout(salida):
            self.assertTrue(auditoria.leerRegistroDesde("07:10:2026"))
        self.assertNotIn("evento_dia_6", salida.getvalue())
        self.assertIn("evento_dia_7", salida.getvalue())
        self.assertIn("evento_dia_8", salida.getvalue())
        with redirect_stdout(io.StringIO()):
            self.assertFalse(auditoria.leerRegistroFecha("09:10:2026"))
        with self.assertRaises(ValueError):
            auditoria.leerRegistroFecha("31:02:2026")

    # Un fallo de acceso se convierte en OSError; no se toca el historial real.
    def test_error_al_escribir_auditoria(self):
        self.preparar_log()
        with patch.object(Path, "open", side_effect=OSError("fallo simulado")):
            with self.assertRaisesRegex(OSError, "No se pudo guardar"):
                auditoria.registrar_evento("red", "evento")

    # Ocho operaciones deben volver al menú si falla el log, conservando el estado.
    def test_menus_manejan_fallos_de_auditoria(self):
        casos = [
            ("login", "menuAutenticacion", ["1", "u", "p", "3"], "tabla_hash.registrar_evento"),
            ("registro", "menuAutenticacion", ["2", "u", "p", "3"], "tabla_hash.registrar_evento"),
            ("carpeta", "menuArchivos", ["1", "docs", "/", "0"], "servidor.registrar_evento"),
            ("archivo", "menuArchivos", ["2", "nuevo.txt", "/", "0"], "servidor.registrar_evento"),
            ("eliminar", "menuArchivos", ["5", "/f", "0"], "servidor.registrar_evento"),
            ("conectar", "menuRed", ["1", "A", "B", "10", "0"], "grafo_red.registrar_evento"),
            ("desconectar", "menuRed", ["2", "A", "B", "0"], "grafo_red.registrar_evento"),
            ("enviar", "menuRed", ["4", "A", "B", "0"], "enrutamiento.registrar_evento"),
        ]
        for nombre, menu, entradas, destino_patch in casos:
            with self.subTest(operacion=nombre):
                servidor = Servidor("A")
                servidor.crear_nodo("f", False)
                servidor.usuarios.registrar_usuario("u", "p")
                red = GrafoRed()
                red.agregar_servidor(servidor)
                red.agregar_servidor(Servidor("B"))
                if nombre in ("desconectar", "enviar"):
                    red.agregar_conexion("A", "B", 10)

                # Para comprobar el registro se usa un usuario que todavía no existe.
                if nombre == "registro":
                    entradas = ["2", "nuevo", "p", "3"]
                conexiones = [lista[:] for lista in red.adyacencias]
                usuarios = [lista[:] for lista in servidor.usuarios.tabla]
                hijos = servidor.raiz.hijos[:]
                argumento = red if menu == "menuRed" else servidor
                salida = io.StringIO()

                with patch.object(main, "limpiarConsola"), \
                        patch.object(main, "pausarConsola"), \
                        patch.object(main, "menuArchivos", wraps=main.menuArchivos) as archivos, \
                        patch("builtins.input", side_effect=entradas), \
                        patch(destino_patch, side_effect=OSError("fallo simulado")) as registrar, \
                        redirect_stdout(salida):
                    getattr(main, menu)(argumento)
                    registrar.assert_called_once()
                    if menu == "menuAutenticacion":
                        archivos.assert_not_called()

                self.assertIn("Error de auditoría:", salida.getvalue())
                self.assertEqual(red.adyacencias, conexiones)
                self.assertEqual(servidor.usuarios.tabla, usuarios)
                self.assertEqual(servidor.raiz.hijos, hijos)


if __name__ == "__main__":
    unittest.main()
