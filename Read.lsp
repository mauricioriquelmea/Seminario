(defun c:ejecutarComandosDesdeArchivo ()
  (setq rutaArchivo "C:/_ Curso/-   Ing. en Comp. e Inf/Cursos/_SEMINARIO DE LICENCIA EN INGENIERIA/Semana 8/Sumativa/Entregable/Python/comandos.txt")  ; Ajusta la ruta al archivo
  (setq archivo (open rutaArchivo "r"))
  (if archivo
    (progn
      (setq linea (read-line archivo))
      (while linea
        ; Asumir que cada línea es un comando completo de AutoCAD
        (command linea)
        (setq linea (read-line archivo))
      )
      (close archivo)
    )
    (princ "\nNo se pudo abrir el archivo.")
  )
  (princ)
)

; Llama a la función automáticamente al cargar el script
(c:ejecutarComandosDesdeArchivo)