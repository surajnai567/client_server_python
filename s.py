import asyncio
import signal
import fileinput
import os
import time
signal.signal(signal.SIGINT, signal.SIG_DFL)


file_location = os.path.join(os.getcwd(), 'Root', 'Admin', 'Register.txt')


class Operational:
    def __init__(self, us):
        self.usi = us
        self.pah = os.path.join(os.getcwd(), 'Root', self.usi)
        try:
            os.makedirs(self.pah)
        except Exception:
            pass
        self.fname = str
        self.true = True
        self.fpah = str
        self.pam = str
        self.path = str
        self.data = str
        self.sze = str
        self.cre = str
        self.mod = str
        self.fol = str
        self.oname = str
        self.nname = str
        self.input = str

    def create_folder(self, name):
        """Creates new folder

        Args:
            name ([str]): [folder name]

        """
        self.fname = name
        self.true = False
        self.fpah = os.path.join(self.pah, self.fname)
        try:
            os.makedirs(self.fpah)
            self.true = True
        except FileExistsError:
            print("File Exists")
        finally:
            return self.true

    def wf(self, fname, name, inputd):
        """writes file

        Args:
            fname ([str]): [folder name]
            name ([str]): [file name]
            inputd ([str]): [data to be entered]
        """
        self.finame = name
        self.fname = f"{fname}\\"
        self.input = inputd
        self.true = False
        try:
            self.pam = os.path.join(self.pah, self.fname)
            self.path = os.path.join(self.pam, self.finame)
            with open(self.path, 'w') as wal:
                wal.write(self.input)
                self.true = True
        except Exception as exp:
            print(exp)
        finally:
            return self.true

    def rf(self, fname, name):
        """reads file

        Args:
            fname ([str]): [folder name]
            name ([str]): [file name]

        Returns:
            [str]: [data]
        """
        self.finame = name
        self.fname = f"{fname}\\"
        self.data = ''
        try:
            self.pam = os.path.join(self.pah, self.fname)
            self.path = os.path.join(self.pam, self.finame)
            with open(self.path, 'r') as red:
                self.data = red.readlines()
        except Exception as exp:
            return print(exp)
        finally:
            return " ".join(self.data)

    def lis(self):
        """gives list of data

        Returns:
            [str]: [List of containing data]
        """
        self.fpah = os.listdir(self.pah)
        self.sze = []
        self.cre = []
        self.mod = []
        total_size = 0
        for fpah in self.fpah:
            self.fol = os.path.join(self.pah, fpah)
            self.mod.append(time.ctime(os.path.getmtime(f"{self.fol}")))
            self.cre.append(time.ctime(os.path.getctime(f"{self.fol}")))
            for path, dirs, files in os.walk(self.fol):
                for fpah in files:
                    fpth = os.path.join(path, fpah)
                    total_size += os.path.getsize(fpth)
            self.sze.append(total_size)
        return self.fpah, self.sze, self.cre, self.mod

    def cf(self, oname, nname):
        """changes directory

        Args:
            oname ([str]): [old name]
            nname ([str]): [new name]

        """
        self.oname = oname
        self.nname = nname
        self.cre = False
        os.chdir(self.pah)
        try:
            os.rename(oname, nname)
            self.cre = True
        except Exception:
            pass
        finally:
            return self.cre

async def register(reader, writer):
    """ This function helps us to register in the log by creating a valid username and password"""

    enter = "Enter your name :"
    writer.write(enter.encode())
    view = await reader.read(100)
    name = view.decode().strip()
    enter = "Create true User Name : "
    writer.write(enter.encode())
    view = await reader.read(100)
    usid = view.decode().strip()
    enter = "Enter your Password :"
    writer.write(enter.encode())
    view = await reader.read(100)
    password = view.decode().strip()
    true = False
    with open(file_location, 'r') as enter:
        for lie in enter:
            if usid in lie:
                if password in lie:
                    true = True
                    break
    if not true:
        with open(file_location, 'a') as w:
            w.write(usid + ':')
            w.write(password + ', \n')
        enter = "User Registered Succcessfully."
        writer.write(enter.encode())
    else:
        enter = "Request Denied\nYou are already Registered"
        writer.write(enter.encode())


async def login(reader, writer):
    """ This function helps us to login and give access to the commands that we declared"""
    enter = """\t\tLogin Form
    Enter UserID   : """
    writer.write(enter.encode())
    view = await reader.read(100)
    usid = view.decode().strip()
    enter = "    Enter Password : "
    writer.write(enter.encode())
    view = await reader.read(100)
    passw = view.decode().strip()
    filepath = file_location
    c = 0
    b = True
    with open(filepath, 'r') as p:
        for line in p:
            if usid in line:
                if passw in line:
                    c = 1
                    if "logged" in line:
                        enter = "You have logged in already\nAccess Denied"
                        writer.write(enter.encode())
                        b = False
                        break

    if b:
        for line in fileinput.FileInput(filepath, inplace=1):
            if usid in line:
                if passw in line:
                    line = line.rstrip()
                    line = line.replace(line, line + "logged\n")
            print(line, end='')
    if c != 1:
        enter = "Invalid Username or Password"
        writer.write(enter.encode())
    elif c == 1 and b:
        try:
            enter = """
            Login Access Granted.\nWelcome\nCommand are:
            1.Create folder
            2.Writefile
            3.Readfile
            4.List directories
            5.Change Foldername
            0.Logout"""
            writer.write(enter.encode())
            user = Operational(usid)
            while True:
                view = await reader.read(100)
                crdch = view.decode().strip()
                if crdch == '1':
                    enter = "Enter folder name : "
                    writer.write(enter.encode())
                    view = await reader.read(100)
                    fname = view.decode().strip()
                    c = user.create_folder(fname)
                    if c:
                        enter = "Folder Created!"
                        writer.write(enter.encode())
                    else:
                        enter = "Folder Exists"
                        writer.write(enter.encode())
                elif crdch == '2':
                    entre = "Enter folder name : "
                    writer.write(entre.encode())
                    d = await reader.read(50)
                    folname = d.decode().strip()
                    entre = "Enter file name : "
                    writer.write(entre.encode())
                    d = await reader.read(50)
                    filename = d.decode().strip()
                    entre = "Enter the data : "
                    writer.write(entre.encode())
                    d = await reader.read(50)
                    id = d.decode().strip()
                    i = user.wf(folname, filename, id)
                    if i:
                        entre = "File Created"
                        writer.write(entre.encode())
                elif crdch == '3':
                    enter = "Enter folder name : "
                    writer.write(enter.encode())
                    view = await reader.read(100)
                    folname = view.decode().strip()
                    enter = "Enter file name : "
                    writer.write(enter.encode())
                    view = await reader.read(100)
                    filename = view.decode().strip()
                    k = user.rf(folname, filename)
                    if k:
                        read = str(user.rf(folname, filename))
                        writer.write(read.encode())
                    else:
                        d = "File doesn't exist"
                        writer.write(d.encode())
                elif crdch == '4':
                    lname, lsize, lcr, lrod = user.lis()
                    enter = "Name      Size         Created           rodified"
                    writer.write(enter.encode())
                    view = await reader.read(100)
                    enter = view.decode().strip()
                    sname = str(" ".join(lname))
                    writer.write(sname.encode())
                    view = await reader.read(100)
                    enter = view.decode().strip()
                    ssize = str(" ".join(map(str, lsize)))
                    writer.write(ssize.encode())
                    view = await reader.read(100)
                    enter = view.decode().strip()
                    scr = str("  ".join(map(str, lcr)))
                    writer.write(scr.encode())
                    view = await reader.read(100)
                    enter = view.decode().strip()
                    srod = str("  ".join(map(str, lrod)))
                    writer.write(srod.encode())
                    view = await reader.read(100)
                    enter = view.decode().strip()
                elif crdch == '5':
                    enter = "Enter Folder name : "
                    writer .write(enter.encode())
                    view = await reader.read(100)
                    oname = view.decode().strip()
                    enter = "Enter new Name : "
                    writer.write(enter.encode())
                    view = await reader.read(100)
                    nname = view.decode().strip()
                    n = user.cf(oname, nname)
                    if n:
                        enter = "Changed Successfully"
                    else:
                        enter = "NO file Exists"
                    writer.write(enter.encode())

                elif crdch == '0':
                    break
        except Exception as e:
            print(e)
        finally:
            for line in fileinput.FileInput(filepath, inplace=1):
                if usid in line:
                    if passw in line:
                        line = line.rstrip()
                        line = line.replace(line, f"{usid}:{passw},\n")
                print(line, end='')
            enter = "Log Out Successfull"
            writer.write(enter.encode())


async def choose(reader, writer):
    """ This function helps us to either register or login if we already registered"""
    ressage = """Choice Register or Login
    1. Register
    2. Login
    Enter your choice :"""
    writer.write(ressage.encode())
    view = await reader.read(100)
    ch = view.decode().strip()
    if ch == '1':
        await register(reader, writer)
    else:
        await login(reader, writer)


async def rain():
    """This function helps us to start the server and run"""
    server = await asyncio.start_server(
        choose, '127.0.0.1', 8898)

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()

asyncio.run(rain())
