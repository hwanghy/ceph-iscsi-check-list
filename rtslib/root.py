 # Fix error reboot
 # Line 167
 
 try:
                fwrite(dbroot_path, self._preferred_dbroot+"\n")
            except:
-                raise RTSLibError("Cannot set dbroot to {}. Please check if this directory exists."
-                                  .format(self._preferred_dbroot))
+                if not os.path.isdir(self._preferred_dbroot):
+                    raise RTSLibError("Cannot set dbroot to {}. Please check if this directory exists."
+                                      .format(self._preferred_dbroot))
            self._dbroot = fread(dbroot_path)

    def _get_dbroot(self):
