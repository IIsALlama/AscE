import pip, os, importlib
def install(package):
    try:
        importlib.import_module(package)
    except ImportError:
        try:
            os.system("pip install " + package)
        except:
            try:
                os.system("pip3 install " + package)
            except:
                print("pip not found")
    finally:
        os.system("pyinstaller --specpath "+ os.getcwd() +"/build --name Build --onefile " + os.getcwd() + "/run.py")
install("pyinstaller")
