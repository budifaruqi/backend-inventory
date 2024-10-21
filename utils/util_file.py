import os


class FileUtil:

    SizeKB = 1024
    SizeMB = SizeKB * 1024
    SizeGB = SizeMB * 1024
    SizeTB = SizeGB * 1024

    CommonMimeTypeExt = [
        ("image/png", "png"),
        ("image/bmp", "bmp"),
        ("text/css", "css"),
        ("text/csv", "csv"),
        ("application/msword", "doc"),
        ("application/vnd.openxmlformats-officedocument.wordprocessingml.document", "docx"),
        ("application/epub+zip", "epub"),
        ("application/gzip", "gzip"),
        ("image/gif", "gif"),
        ("text/html", "html"),
        ("text/html", "htm"),
        ("image/vnd.microsoft.icon", "ico"),
        ("application/java-archive", "jar"),
        ("image/jpeg", "jpeg"),
        ("image/jpeg", "jpg"),
        ("text/javascript", "js"),
        ("application/json", "json"),
        ("audio/mpeg", "mp3"),
        ("video/mp4", "mp4"),
        ("video/mpeg", "mpeg"),
        ("audio/opus", "opus"),
        ("image/png", "png"),
        ("application/pdf", "pdf"),
        ("application/vnd.ms-powerpoint", "ppt"),
        ("application/vnd.openxmlformats-officedocument.presentationml.presentation", "pptx"),
        ("application/vnd.rar", "rar"),
        ("application/rtf", "rtf"),
        ("application/x-sh", "sh"),
        ("image/svg+xml", "svg"),
        ("application/x-tar", "tar"),
        ("image/tiff", "tiff"),
        ("image/tiff", "tif"),
        ("text/plain", "txt"),
        ("audio/wav", "wav"),
        ("audio/webm", "weba"),
        ("video/webm", "webm"),
        ("image/webp", "webp"),
        ("application/xhtml+xml", "xhtml"),
        ("application/vnd.ms-excel", "xls"),
        ("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "xlsx"),
        ("application/xml", "xml"),
        ("application/zip", "zip"),
        ("application/x-7z-compressed", "7z")
    ]

    @staticmethod
    def PrettyFileSize(size: int) -> str:
        if size <= 0:
            return "0 B"
        elif size < FileUtil.SizeKB:
            return f"{size} B"
        elif size < FileUtil.SizeMB:
            return f"{round(size / FileUtil.SizeKB, 2)} KB"
        elif size < FileUtil.SizeGB:
            return f"{round(size / FileUtil.SizeMB, 2)} MB"
        elif size < FileUtil.SizeTB:
            return f"{round(size / FileUtil.SizeGB, 2)} GB"
        else:
            return f"{round(size / FileUtil.SizeTB, 2)} TB"

    @staticmethod
    def ExtractFileExtension(s: str) -> str | None:
        _, fileExt = os.path.splitext(s)
        if (fileExt == ""):
            return None
        return fileExt

    @staticmethod
    def RemoveFile(s: str) -> bool:
        try:
            os.remove(s)
            return True
        except:
            return False

    @staticmethod
    def RemoveDirectory(s: str) -> bool:
        try:
            os.rmdir(s)
            return True
        except:
            return False

    # @staticmethod
    # def CreateDirectory(rootPath: str) -> Union[bool, str]:
    #     if rootPath.startswith("./"):
    #         rootPath = rootPath.replace("./", "", 1)
    #     try:
    #         arr = rootPath.split("/")
    #         s = "."
    #         for i in range(len(arr)):
    #             t = arr[i].strip()
    #             if t == "":
    #                 continue
    #             s += "/" + t
    #             if os.path.isdir(s):
    #                 continue
    #             os.mkdir(s)
    #     except:
    #         return False
    #     return s

    @staticmethod
    def CreateDirectory(rootPath: str) -> str | None:
        if rootPath.startswith("./"):
            rootPath = rootPath.replace("./", "", 1)
            s = "."
        elif rootPath.startswith("/"):
            rootPath = rootPath.replace("/", "", 1)
            s = ""
        elif rootPath.startswith("~/"):
            rootPath = rootPath.replace("~/", "", 1)
            s = "~"
        else:
            return None
        try:
            arr = rootPath.split("/")
            for i in range(len(arr)):
                t = arr[i].strip()
                if t == "":
                    continue
                s += "/" + t
                if os.path.isdir(s):
                    continue
                os.mkdir(s)
        except Exception as err:
            print("CreateDirectory error:", str(err), "target:", s)
            return None
        return s

    @staticmethod
    def MimeTypeToFileExtension(mime: str | None) -> str | None:
        if mime is None:
            return None
        mime = mime.lower()
        for a in FileUtil.CommonMimeTypeExt:
            if a[0] == mime:
                return a[1]
            
        return None
    
    @staticmethod
    def FileExtensionToMimeType(ext: str | None) -> str | None:
        if ext is None:
            return None
        ext = ext.lower()
        for a in FileUtil.CommonMimeTypeExt:
            if a[1] == ext:
                return a[0]
            
        return None
    
    @staticmethod
    def NormalizeFilename(filename: str) -> str:
        normalizedName = ""
        for s in filename:
            c = ord(s)
            if (((c >= 48) and (c <= 57)) or    # 0..9
                ((c >= 65) and (c <= 90)) or    # A..Z
                ((c >= 87) and (c <= 122)) or   # a..z
                (c == 45) or                    # -
                (c == 95)                       # _
            ):
                normalizedName += s
            elif (c == 32):
                normalizedName += "_"
        return normalizedName
    
    @staticmethod
    def SaveToFile(path: str | None, filename: str, data: bytes) -> bool:
        try:
            target = ""
            if path is not None:
                if not FileUtil.CreateDirectory(path):
                    print(f"SaveToFile::Cannot create directory {str(path)}")
                    return False
                target = path
            
            if not target.endswith(os.sep):
                target += os.sep
            target += filename

            with open(target, "wb") as f:
                f.write(data)
            return True
        except Exception as err:
            print("Save ticket failed " + str(err))
            return False