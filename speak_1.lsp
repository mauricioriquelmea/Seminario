
(vl-load-com)

(if (= (getvar "LOCALE") "CSY"); auto language-switch
 (setq
   sp_whoami "\nMluv�c� AutoCAD - zkuste kreslit do zam�en� hladiny, zadat neexistuj�c� p��kaz nebo p�e��kat seznam hladin p��kazem LAYTALK, p��kaz SAY, QUIET (CAD Studio - www.cadstudio.cz)"
   sp_unknown "Neznaamy pzhikaz"
   sp_nolock "Namu-zhe-tae kreslit doe zamchana hlaedeeny!"
   sp_laylist "Seznam ladin:"
 )
 (setq 
   sp_whoami "\nTalking AutoCAD - try to draw on a locked layer, enter a non-existing command or let AutoCAD say the layer names with the LAYTALK command, command SAY, QUIET (CAD Studio - www.cadstudio.cz)"
   sp_unknown "Unknown command"
   sp_nolock "Cannot draw on a locked layer!"
   sp_laylist "Layer list:"
 )
);if

;----

(defun sp_talk (text / sapi); internal talk function
 (if (not sp_quiet)
  (progn
   (setq sapi (vlax-create-object "Sapi.SpVoice"))
   (vlax-put sapi 'SynchronousSpeakTimeout 1) ; ms
   (vlax-invoke-method sapi 'WaitUntilDone 1) ; ms
   (vlax-invoke sapi "Speak" text 0) ; 8=XML?
   (vlax-release-object sapi)
 ))
)

(if (not sp_react)
  (setq sp_react (vlr-command-reactor nil ; command reactors
     (list (cons :vlr-commandWillStart (function sp_autocad_startcmd))
					 (cons :vlr-unknownCommand   (function sp_autocad_unknowncmd))
					 (cons :vlr-commandEnded     (function sp_autocad_endcmd))
			)
    )
  )
);react

(defun sp_autocad_startcmd (react cmd / clayer ent)
;  (sp_talk (strcat "Starting " (car cmd)))
  (sp_talk (car cmd)) ; tell the command name
  (setq clayer (getvar "CLAYER"))
  (setq ent (entget (tblobjname "LAYER" clayer)))
  (setq layp (cdr (assoc 70 ent)))
  (if (and (= layp 4) (member (car cmd) '("LINE" "CIRCLE" "ARC" "TEXT" "MTEXT" "ELLIPSE" "PLINE" "SPLINE" "INSERT" "POINT" "HATCH")))
   (sp_talk sp_nolock)
  );
)
(defun sp_autocad_unknowncmd (react cmd)
  (sp_talk (strcat sp_unknown " " (car cmd)))
)
(defun sp_autocad_endcmd (react cmd)
;  (sp_talk (strcat "Finished " (car cmd)))
 (princ)
)


(defun C:LAYTALK ( / laylist layname) ; talk layers
    (sp_talk sp_laylist)
    (setq layname (cdr (assoc 2 (tblnext "LAYER" T))))
    (print layname)
    (sp_talk layname)
    (while (setq layname (cdr (assoc 2 (tblnext "LAYER"))))
      (print layname)
      (sp_talk layname)
    )
 (prin1)
 )

(defun C:SAY () ; say something
 (setq s (getstring "What to say: " T))
 (sp_talk s)
 (princ)
)

(defun C:QUIET () ; quiet toggle
 (if sp_quiet
  (progn (setq sp_quiet nil)(sp_talk(princ "Now will talk...")))
  (progn (sp_talk(princ "Now will be quiet..."))(setq sp_quiet T))
 )
 ;(setq sp_quiet (not sp_quiet))
 (princ)
)


(princ sp_whoami)
(prin1)