from typing import Any
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
        pickle.dump(self.__get_store(), open(self.path, "wb"))


    def __load(self) -> object:
        try:
            return pickle.load(open(self.path, "rb")) 
        except:
            return self.cls()


    def __init__(self, cls, path) -> None:

        self.cls    = cls
        self.path   = path

        if not hasattr(self.__class__, self.__get_store_name()):
            setattr(self.__class__, self.__get_store_name(), self.__load())


    def get_element(self, __name: str) -> Any:
        return self.__get_store().__getattribute__(__name)


    def set_element(self, __name: str, __value: Any) -> None:
        if self.__get_store().__getattribute__(__name) != __value:
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
