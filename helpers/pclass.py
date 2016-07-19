# -*- coding: utf-8 -*-
import abc
import constants


class Group(metaclass=abc.ABCMeta):
    __slots__ = ["id"]

    @abc.abstractclassmethod
    def get_members(self, count, offset=0, limit=constants.MAX_GROUP_MEMBERS, **options):
        """

        :rtype: Users
        """
        pass

    @abc.abstractclassmethod
    def __len__(self):
        """

        :rtype: int
        """
        pass


class Users(metaclass=abc.ABCMeta):
    __slots__ = ["ids"]

    @abc.abstractclassmethod
    def get_information(self, **options):
        """

        :rtype: list of User objects
        """
        pass


class User(metaclass=abc.ABCMeta):
    __slots__ = ["id"]

    @abc.abstractclassmethod
    def get_information(self, **options):
        pass

    @abc.abstractclassmethod
    def get_audio(self, **options):
        pass

    @abc.abstractclassmethod
    def get_wall(self, **options):
        pass

    @abc.abstractclassmethod
    def get_friends(self, **options):
        pass

    @abc.abstractclassmethod
    def get_groups(self, **options):
        pass
