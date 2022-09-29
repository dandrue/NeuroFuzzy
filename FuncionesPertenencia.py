#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 23:21:39 2021

@author: diego
"""
import numpy as np
import statistics 


class TrapAbiertaIzquierda:
    """Clase para generar una función de pertenencia Trapezoidal Abierta a la Izquierda, requiere de los siguientes
    parámetros:
            nombre: El nombre de la función
            inicio: Valor de inicio
            medio: Valor medio de la función, donde termina la sección horizontal e inicia la pendiente
            fin: Valor de fin de la función
            altura: altura de la función

    Parameters
    ----------

    Returns
    -------

    """
    
    def __init__(self, nombre, var, param, altura=1):
        self.nombre = nombre
        self.var = var
        self.param = param
        self.type = "TrapAbiertaIzquierda"
        self.inicio = self.param[0]
        self.medio = self.param[1]
        self.fin = self.param[2]
        self.altura = altura
        self.x, self.y = self.update()

    def update(self):
        """ """
        self.inicio = self.param[0]
        self.medio = self.param[1]
        self.fin = self.param[2]
        increment = 0.5
        x = np.arange(self.inicio, self.fin+increment, increment)
        # for i in x:
        #     print(i)
        y = []
        for i in x:
            if i <= self.medio:
                y.append(self.altura)
            elif i > self.medio:
                m = (self.altura-0)/(self.medio-self.fin)
                y.append(m*i-m*self.fin)
        # print("Regla trapezoidal izquierda abierta creada")
        y = np.array(y)
        # print(x,y)
        self.x = x
        self.y = y
        return self.x, self.y
        
    def eval(self, entry):
        """

        Parameters
        ----------
        entry :
            

        Returns
        -------

        """
        medio = self.medio
        fin = self.fin
        inicio = self.inicio
        altura = self.altura
        i = entry
        pertenencia = 0
        if round(inicio, 0) <= entry <= round(fin, 0):
            if i > medio:
                m = (altura-0)/(medio-fin)
                pertenencia = m*i-m*fin
            elif i <= medio:
                pertenencia = altura
            pertenencia = round(pertenencia, 5)
        else:
            pertenencia = 0
        return pertenencia
    
    def evalx(self, pertenencia):
        """

        Parameters
        ----------
        pertenencia :
            

        Returns
        -------

        """
        medio = self.medio
        fin = self.fin
        altura = self.altura
        m = (altura-0)/(medio-fin)
        x = (pertenencia + (m*fin))/m
        x = round(x, 5)
        return x
        
        
class TrapAbiertaDerecha:
    """ """
    def __init__(self, nombre, var, param, altura=1):
        self.nombre = nombre
        self.var = var
        self.param = param
        self.type = "TrapAbiertaDerecha"
        self.inicio = self.param[0]
        self.medio = self.param[1]
        self.fin = self.param[2]
        self.altura = altura
        self.x, self.y = self.update()

    def update(self):
        """ """
        self.inicio = self.param[0]
        self.medio = self.param[1]
        self.fin = self.param[2]
        increment = 0.5
        x = np.arange(self.inicio, self.fin+increment, increment)
        # for i in x:
        #    print(i)
        y = []
        for i in x:
            if i >= self.medio:
                y.append(self.altura)
            elif i < self.medio:
                m = (0-self.altura)/(self.inicio-self.medio)
                y.append(m*i-m*self.inicio)
        # print("Regla trapezoidal derecha abierta creada")
        y = np.array(y)
        # print(x,y)
        self.x = x
        self.y = y
        return self.x, self.y
        
    def eval(self, entry):
        """

        Parameters
        ----------
        entry :
            

        Returns
        -------

        """
        medio = self.medio
        fin = self.fin
        inicio = self.inicio
        altura = self.altura
        i = entry
        pertenencia = 0
        if round(inicio, 0) <= entry <= round(fin, 0):
            if i >= medio:
                pertenencia = altura
            elif i < medio:
                m = (0-altura)/(inicio-medio)
                pertenencia = (m*i-m*inicio)
            pertenencia = round(pertenencia, 5)
        else:
            pertenencia = 0
        return pertenencia
    
    def evalx(self, pertenencia):
        """

        Parameters
        ----------
        pertenencia :
            

        Returns
        -------

        """
        medio = self.medio
        inicio = self.inicio
        altura = self.altura
        m = (0-altura)/(inicio-medio)
        x = (pertenencia + (m*inicio))/m
        x = round(x, 5)
        return x    


class Trapezoidal:
    """ """
    def __init__(self, nombre, var, param, altura=1):
        self.nombre = nombre
        self.var = var
        self.param = param
        self.type = "Trapezoidal"
        self.inicio = self.param[0]
        self.medio1 = self.param[1]
        self.medio2 = self.param[2]
        self.fin = self.param[3]
        self.altura = altura
        self.x, self.y = self.update()

    def update(self):
        """ """
        self.inicio = self.param[0]
        self.medio1 = self.param[1]
        self.medio2 = self.param[2]
        self.fin = self.param[3]
        increment = 0.5
        x = np.arange(self.inicio, self.fin+increment, increment)
        y = []
        for i in x:
            if i > self.medio2:
                m = (self.altura-0)/(self.medio2-self.fin)
                y.append(m*i-m*self.fin)
            elif self.medio1 <= i <= self.medio2:
                y.append(self.altura)
            elif i < self.medio1:
                m = (0-self.altura)/(self.inicio-self.medio1)
                y.append(m*i-m*self.inicio)
        # print("Regla trapezoidal cerrada creada")
        y = np.array(y)
        # print(x,y)
        self.x = x
        self.y = y
        return self.x, self.y
        
    def eval(self, entry):
        """

        Parameters
        ----------
        entry :
            

        Returns
        -------

        """
        medio1 = self.medio1
        medio2 = self.medio2
        fin = self.fin
        inicio = self.inicio
        altura = self.altura
        i = entry
        pertenencia = 0
        if round(inicio, 0) <= entry <= round(fin, 0):
            if i > medio2:
                m = (altura-0)/(medio2-fin)
                pertenencia = (m*i-m*fin)
            elif medio1 <= i <= medio2:
                pertenencia = altura
            elif i < medio1:
                m = (0-altura)/(inicio-medio1)
                pertenencia = (m*i-m*inicio)
            pertenencia = round(pertenencia, 5)
        else:
            pertenencia = 0
        return pertenencia
    
    def evalx(self, entry):
        """

        Parameters
        ----------
        entry :
            

        Returns
        -------

        """
        inicio = self.inicio
        medio1 = self.medio1
        medio2 = self.medio2
        altura = self.altura
        fin = self.fin
        m1 = (0-altura)/(inicio-medio1)
        x1 = (entry+m1*inicio)/m1
        m2 = (altura-0)/(medio2-fin)
        x2 = (entry+m2*fin)/m2
        return x1, x2


class Triangular:
    """ """
    def __init__(self, nombre, var, param, altura=1):
        self.nombre = nombre
        self.var = var
        self.param = param
        self.type = "Triangular"
        self.inicio = self.param[0]
        self.medio = self.param[1]
        self.fin = self.param[2]
        self.altura = altura
        self.x, self.y = self.update()

    def update(self):
        """ """
        self.inicio = self.param[0]
        self.medio = self.param[1]
        self.fin = self.param[2]
        increment = 0.5
        x = np.arange(self.inicio, self.fin+increment, increment)
        # for i in x:
        # print(i)
        y = []
        for i in x:
            if i >= self.medio:
                m = (self.altura-0)/(self.medio-self.fin)
                y.append(m*i-m*self.fin)
            elif i < self.medio:
                m = (0-self.altura)/(self.inicio-self.medio)
                y.append(m*i-m*self.inicio)
        # print("Regla triangular cerrada creada")
        y = np.array(y)
        # print(x,y)
        self.x, self.y = x, y
        return self.x, self.y
        
    def eval(self, entry):
        """

        Parameters
        ----------
        entry :
            

        Returns
        -------

        """
        medio = self.medio
        fin = self.fin
        inicio = self.inicio
        altura = self.altura
        i = entry
        pertenencia = 0
        if round(inicio, 0) <= entry <= round(fin, 0):
            if i >= medio:
                m = (altura-0)/(medio-fin)
                pertenencia = m * i - m * fin
            elif i < medio:
                m = (0-altura)/(inicio-medio)
                pertenencia = (m * i - m * inicio)
            pertenencia = round(pertenencia, 5)
        else:
            pertenencia = 0
        return pertenencia
    
    def evalx(self, entry):
        """

        Parameters
        ----------
        entry :
            

        Returns
        -------

        """
        inicio = self.inicio
        medio = self.medio
        fin = self.fin
        altura = self.altura
        m1 = (0-altura)/(inicio-medio)
        x1 = (entry+m1*inicio)/m1
        m2 = (altura-0)/(medio-fin)
        x2 = (entry+m2*fin)/m2
        return x1, x2


class Intersecciones:
    """ """
    @staticmethod
    def zadeh(lista):
        """

        Parameters
        ----------
        lista :
            

        Returns
        -------

        """
        interseccion = min(lista)
        return interseccion

    @staticmethod
    def mean(lista):
        """

        Parameters
        ----------
        lista :
            

        Returns
        -------

        """
        interseccion = statistics.mean(lista)
        return interseccion

    @staticmethod
    def larsen(lista):
        """

        Parameters
        ----------
        lista :
            

        Returns
        -------

        """
        interseccion = 1
        for i in lista:
            interseccion = interseccion * i
        return interseccion

    @staticmethod
    def binary(lista):
        """

        Parameters
        ----------
        lista :
            

        Returns
        -------

        """
        interseccion = max(1-lista[0], lista[1])
        return interseccion


class Conorma:
    """ """
    @staticmethod
    def max(lista):
        """

        Parameters
        ----------
        lista :
            

        Returns
        -------

        """
        value = max(lista)
        return value

    @staticmethod
    def sum(lista):
        """

        Parameters
        ----------
        lista :
            

        Returns
        -------

        """
        value = sum(lista)
        if value > 1:
            value = 1
        return value
