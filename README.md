# STOCKY IA

**Predicción de demanda de productos en empresas retail con IA y un asistente conversacional.**

## 🛠 Problemática  

Las empresas retail enfrentan serios desafíos para gestionar su inventario de manera eficiente debido a:  
- **Predicciones inexactas** de la demanda de productos, lo que genera errores en la planificación.  
- **Sobreabastecimiento o desabastecimiento**, causando pérdidas económicas o insatisfacción de los clientes.  
- **Falta de herramientas accesibles y fáciles de usar** para visualizar datos históricos y proyecciones futuras.  
- **Dificultad para interpretar los resultados de la IA**, ya que los responsables del negocio no siempre son expertos en análisis de datos.  

---

## 🎯 Objetivo del Proyecto  

**STOCKY IA** busca desarrollar una **aplicación web inteligente** que:  
1. **Prediga la demanda de productos** utilizando modelos avanzados de inteligencia artificial (LSTM, Prophet y Darts).  
2. **Permita la carga y entrenamiento de datasets** a través de archivos CSV.  
3. **Muestre dashboards interactivos** con predicciones históricas y futuras.  
4. **Explique los resultados mediante un asistente conversacional AI**, ayudando a entender y confiar en las predicciones.  
5. **Genere reportes descargables** (PDF o Excel) para apoyar la toma de decisiones.  

---

## 💡 Solución Propuesta  

- **Backend (FastAPI):** Proporciona los endpoints para predicción, carga de datos y entrenamiento asíncrono (Celery + Redis).  
- **Frontend (Angular):** Ofrece una interfaz moderna, intuitiva y responsiva para interactuar con los modelos.  
- **Chatbot AI:** Explica las predicciones y da recomendaciones usando OpenAI.  
- **Arquitectura Escalable:** Basada en microservicios y contenedores para despliegue en la nube.  


## 🚀 Tecnologías
- **Frontend:** Angular 17
- **Backend:** FastAPI (Python 3.11)
- **Asíncrono:** Celery + Redis
- **Base de Datos:** PostgreSQL
- **Machine Learning:** TensorFlow + Prophet + Darts
- **Chatbot AI:** OpenAI API

---

## 📊 Dashboard  
El dashboard en Angular permite visualizar **predicciones históricas y futuras**, ofreciendo gráficos interactivos y datos fáciles de interpretar para la toma de decisiones.

---

## 🤖 Chatbot AI  
Conecta con **OpenAI** para explicar las predicciones, dar contexto sobre las tendencias y resolver dudas del usuario en un lenguaje sencillo y útil.

---

## ✍️ Autores  
- **Anthony** – Project Manager  
- **Bryam** – Frontend Developer  
- **Erick** – Chatbot Developer  
- **Henry** – Backend Developer  


