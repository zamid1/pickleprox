from typing import Any
import os
import pickle

class PickleProxManager(object):

    """ 
    Proxy Manager class wrapping the pickle interaction.
    -   it will have every backing store object as singleton via class attribute
    -   it will persist backing store on value change only
    """

    def __get_store_name(self) -> str:
        return 'store_' + self.cls.__name__


    def __get_store(self) -> object:
        return getattr(self.__class__, self.__get_store_name())


    def __persist(self) -> None:
        pickle.dump(self.__get_store().__dict__, open(self.path, "wb"))
        self.stamp = os.stat(self.path).st_mtime


    def __overload(self, inst: object) -> None:
        if self.stamp != os.stat(self.path).st_mtime:
            try:
                inst.__dict__ = pickle.load(open(self.path, "rb")) 
            except:
                pass
            else:
                self.stamp = os.stat(self.path).st_mtime

    def __load(self) -> object:
        inst = self.cls()
        self.__overload(inst)
        return inst

    def __init__(self, cls, path) -> None:

        self.cls    = cls
        self.path   = path
        self.stamp  = None

        if not hasattr(self.__class__, self.__get_store_name()):
            setattr(self.__class__, self.__get_store_name(), self.__load())


    def get_element(self, __name: str) -> Any:
        self.__overload(self.__get_store())
        return self.__get_store().__getattribute__(__name)


    def set_element(self, __name: str, __value: Any) -> None:
        if self.__get_store().__getattribute__(__name) != __value:
            self.__overload(self.__get_store())
            self.__get_store().__setattr__(__name, __value)
            self.__persist()



class PickleProx(object):

    """ 
    Proxy class to route all attributes requested to get or set to manager
    """

    def __init__(self, cls, path) -> None:
        object.__setattr__(self, 'manager', PickleProxManager(cls, path))


    def __getattr__(self, __name: str) -> Any:
        return object.__getattribute__(self, 'manager').get_element(__name)


    def __setattr__(self, __name: str, __value: Any) -> None:
        object.__getattribute__(self, 'manager').set_element(__name, __value)
