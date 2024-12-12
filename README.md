# Adaptación de textos para aprendizaje de inglés como lengua extranjera

## Introducción

En el marco de la materia optativa Text Mining, se nos asignó la tarea de desarrollar un proyecto aplicando Inteligencia Artificial con un enfoque en Aprendizaje No Supervisado. El proyecto que elegí aborda el desafío de adaptar textos a un nivel CEFR (Common European Framework of Reference for Languages) dado, con el objetivo principal de identificar configuraciones (modelos, prompts, etc.) que permitan generar adaptaciones satisfactorias a un nivel específico.

Para este trabajo, colaboré con Eli Comelles, integrante del proyecto TaskGen de la Universidad de Barcelona, quien desempeñó el rol de Product Owner y brindó orientación a lo largo del desarrollo.

### Problemática

En el contexto de la enseñanza del inglés como lengua extranjera, los estudiantes suelen tener distintos niveles de competencia en el idioma. Esto genera la necesidad de adaptar materiales educativos, de modo que un mismo texto pueda ser utilizado por alumnos con diferentes niveles, conservando la misma información pero ajustando su complejidad al nivel CEFR correspondiente.

### Datos utilizados

Para llevar a cabo este proyecto, se empleó el dataset CEFR Levelled English Texts, disponible en Kaggle, que contiene 1,493 textos de diversas naturalezas (diálogos, descripciones, historias cortas, artículos de periódico, entre otros). Este dataset incluye una clasificación de los textos en niveles CEFR, orientada a tareas de comprensión lectora.

El CEFR clasifica las competencias lingüísticas en tres grandes categorías: Usuario Básico (A), Usuario Independiente (B) y Usuario Avanzado (C), las cuales se subdividen en seis niveles: A1, A2, B1, B2, C1 y C2.

### División del trabajo

El proyecto se desarrolló en dos etapas principales:

Exploración inicial mediante clasificación de textos: Se investigó la capacidad de modelos de lenguaje para clasificar textos existentes en los niveles CEFR.
Adaptación de textos a niveles específicos CEFR: A partir de los hallazgos de la primera etapa, se trabajó en configurar modelos y prompts para lograr adaptaciones satisfactorias.

## Fase 1: Clasificación de textos en niveles CEFR

### Introducción

La etapa de clasificación se realizó inicialmente para explorar la dificultad del problema, establecer límites y definir expectativas. Este proceso permitió investigar el comportamiento de diferentes modelos y ajustar parámetros, con el objetivo de descartar aproximaciones que no aportaran beneficios significativos. Además, sirvió para identificar un clasificador confiable que pudiera utilizarse para extender la muestra y generar datos adicionales necesarios para realizar el fine-tuning.

Durante esta exploración, se detectaron sesgos propios de algunos modelos que no habrían sido evidentes sin esta etapa. Por ejemplo, en el modelo Llama 3.1, probablemente debido a los datos en los que fue entrenado, se identificó una tendencia a clasificar textos en categorías que contienen el número "2" (A2, B2, C2), siendo especialmente predominante la categoría B2.

### Variables experimentales y métricas utilizadas

**Modelos**  
Se seleccionaron los modelos Llama 3.1 8B y Orca 2 7B debido a su destacado rendimiento en métricas relevantes para el problema de lenguaje natural. Llama 3.1 8B obtiene altos puntaje en IFEval, un benchmark que evalúa la habilidad de seguir instrucciones explícitas, mientras que Orca 2 7B destaca en MuSR, un benchmark que evalúa la integración de el razonamiento en contextos extensos. Estas métricas fueron consideradas de interés para los objetivos del proyecto.

**Prompts utilizados**  
Se exploraron varias configuraciones de prompts para evaluar su impacto en la clasificación de textos:

- 0-shot / few-shot:  
En 0-shot, se pidió directamente realizar la tarea sin proporcionar ejemplos previos.  
En few-shot, se incluyeron algunos ejemplos en el prompt para posiblemente mejorar el rendimiento. En 1-shot y 2-shot, se utilizó un ejemplo por categoría para evitar sesgos.

- Con / Sin lectocomprensión:  
Se especificó si los textos debían clasificarse según criterios de lectocomprensión o no, ya que el nivel CEFR puede variar dependiendo de si los textos son para comprensión lectora o si son producidos por estudiantes.
  
- Con / Sin corrección de sesgo / excluyendo B2:  
Se incluyó en el prompt una advertencia sobre posibles sesgos y se solicitó corregirlos. Para few-shot, también se exploró excluir ejemplos de la clase B2, la categoría que los modelos tendían a predecir con mayor frecuencia, según hallazgos previos.
  
- Con / Sin descriptores de nivel:  
Se añadieron descriptores específicos sobre las características que deben cumplir los textos para cada nivel CEFR. Estos descriptores fueron proporcionados por expertos del proyecto TaskGen 2.
  
- Prompts basados en criterios de enseñanza de lenguas:  
Diseñados por expertos del proyecto TaskGen 2, estos prompts se fundamentaron en principios pedagógicos.

### Métricas de evaluación

Para evaluar el rendimiento de los modelos y las configuraciones de prompt, se utilizaron las siguientes métricas:

- Accuracy, Macro-F1, Micro-F1: Miden el rendimiento general del modelo en términos de predicciones correctas y equilibrio entre clases.
- Accuracy pesada: Ajusta el error en función de la distancia entre las clases. Por ejemplo: Si la etiqueta real es B2 y la predicción es A2, el error es 2. Los aciertos se ponderan con un peso óptimo establecido empíricamente en 2 tras explorar valores entre 1 y 10. La métrica se calcula como la proporción ponderada de aciertos sobre el total de aciertos y errores.
- Accuracy aproximada: Una variante de la accuracy estándar, donde si la predicción está a una distancia de 1 de la clase real (por ejemplo, real: B1, predicción: A2), se otorga un puntaje parcial de 0.5 en lugar de 0.
- Métricas por clase: Cantidad de predicciones, Precisión, Recall

De todas las métricas, las más útiles fueron la accuracy, accuracy aproximada y la Cantidad de predicciones por clase, ya que permitieron descartar aproximaciones con baja precisión respecto a un caso base o con sesgos marcados.

### Experimentos

#### Preparación de los datos

Se equilibraron las clases del dataset para contar con 200 muestras por categoría, lo cual mitigó un sesgo significativo detectado en una exploración preliminar.

El dataset fue dividido en un 80% para entrenamiento, 10% para evaluación, y 10% para holdout. Para garantizar la replicabilidad, se utilizó una semilla fija durante la partición.

#### Exploración inicial y entorno de experimentación

Las primeras exploraciones se realizaron en Google Colab para analizar el dataset y los modelos seleccionados. Posteriormente, los experimentos fueron ejecutados en el CCAD para aprovechar recursos computacionales más robustos.

Antes de utilizar la mayor parte del dataset (90%), se realizó una exploración anecdótica con una pequeña cantidad de muestras. Esta fase permitió:

- Identificar el potencial de ciertos prompts basados en criterios de enseñanza, que incluso superaron las hipótesis iniciales sobre el rendimiento de ejemplos few-shot.
- Concluir que los prompts con descriptores de nivel, a pesar de su mayor longitud, obtuvieron peores resultados en comparación con prompts más simples como los de 2-shot.
- Detectar problemas específicos con el modelo Orca, que generaba texto irrelevante sin proporcionar una clasificación.
Este problema llevó a Ajustar los prompts para mejorar la salida del modelo. Introducir una nueva clase "unknown", que incluye muestras donde no se identificó una clasificación válida.

#### Diseño de experimentos de clasificación
Se llevaron a cabo un total de 23 experimentos por modelo (Orca y Llama), además de 2 experimentos con modelos BERT preentrenados: tareknaous/readabert-en (BERT-Ta) y AbdulSami/bert-base-cased-cefr (BERT-Ab). Todos los propmts utilizados se encuentran en esta [planilla](https://github.com/juan-oviedo/Adaptacion-de-textos-para-aprendizaje-de-ingles-como-lengua-extranjera/blob/main/Experimentos/Experimentos%20Clasificacion.xlsx)

**Desglose de experimentos**  
- 0-shot:  
5 experimentos utilizando prompts basados en criterios de enseñanza.  
2 experimentos con prompts que incluyen descriptores de nivel, uno de ellos con corrección de sesgo excluyendo B2.  
4 experimentos combinando las opciones de sin/con lectocomprensión y sin/con corrección de sesgo.  

- 1-shot:  
4 experimentos combinando las opciones de sin/con lectocomprensión y sin/con corrección de sesgo.  
2 experimentos combinando sin/con lectocomprensión, excluyendo ejemplos de B2.  

- 2-shot:  
Se repitieron las mismas combinaciones exploradas en la configuración de 1-shot.  

- Modelos adicionales:  
Se realizaron experimentos con modelos preentrenados: BERT-Ta y BERT-Ab, conocidos por su capacidad en tareas de clasificación.

#### Evaluación y uso del dataset
Todos los experimentos se realizaron utilizando el 90% del dataset (entrenamiento + evaluación), con el propósito de evaluar los resultados de forma integral.

### Resultados
Las métricas sin procesar están disponibles en esta [planilla](https://github.com/juan-oviedo/Adaptacion-de-textos-para-aprendizaje-de-ingles-como-lengua-extranjera/blob/main/Resultados/Resultados%20Clasificacion.xlsx) de resultados.

Los hallazgos más relevantes se resumen en las siguientes tablas:

| Modelo   | Lecto Comprensión | Corrección       | Few-Shots | Accuracy  | Accuracy Aproximada | Accuracy Pesada | F1 Macro | F1 Micro |
|----------|--------------------|------------------|-----------|-----------|---------------------|-----------------|----------|----------|
| llama    | sí                 | sacando B2       | 2         | 41,65%    | 64,17%              | 53,26%          | 40,62%   | 41,65%   |
| llama    | sí                 | sin              | 2         | 39,54%    | 62,11%              | 50,74%          | 35,52%   | 39,54%   |
| llama    | sí                 | con              | 2         | 39,36%    | 61,24%              | 50,20%          | 34,70%   | 39,36%   |
| llama    | no                 | sacando B2       | 2         | 38,26%    | 59,04%              | 47,60%          | 36,32%   | 38,26%   |
| llama    | sí                 | sin              | 1         | 36,42%    | 58,99%              | 46,68%          | 33,03%   | 36,42%   |
| llama    | no                 | con              | 2         | 36,42%    | 57,89%              | 45,63%          | 32,89%   | 36,42%   |
| llama    | sí                 | sacando B2       | 1         | 36,24%    | 59,63%              | 47,11%          | 36,02%   | 36,24%   |
| llama    | no                 | sin              | 2         | 35,50%    | 57,57%              | 44,61%          | 31,19%   | 35,50%   |
| bert TA  |                    |                  |           | 34,95%    | 62,11%              | 47,83%          | 27,48%   | 34,95%   |
| llama    | no                 | sacando B2       | 1         | 32,39%    | 53,17%              | 39,95%          | 31,18%   | 32,39%   |

Tabla 1: Los 10 mejores experimentos ordenados segun su accuracy.

| Modelo   | Lecto Comprensión | Corrección       | Few-Shots | Accuracy  | Accuracy Aproximada | Accuracy Pesada | F1 Macro | F1 Micro |
|----------|--------------------|------------------|-----------|-----------|---------------------|-----------------|----------|----------|
| llama    | sí                 | sacando B2       | 2         | 41,65%    | 64,17%              | 53,26%          | 40,62%   | 41,65%   |
| llama    | sí                 | sin              | 2         | 39,54%    | 62,11%              | 50,74%          | 35,52%   | 39,54%   |
| bert TA  |                    |                  |           | 34,95%    | 62,11%              | 47,83%          | 27,48%   | 34,95%   |
| llama    | sí                 | con              | 2         | 39,36%    | 61,24%              | 50,20%          | 34,70%   | 39,36%   |
| llama    | sí                 | sacando B2       | 1         | 36,24%    | 59,63%              | 47,11%          | 36,02%   | 36,24%   |
| llama    | no                 | sacando B2       | 2         | 38,26%    | 59,04%              | 47,60%          | 36,32%   | 38,26%   |
| llama    | sí                 | sin              | 1         | 36,42%    | 58,99%              | 46,68%          | 33,03%   | 36,42%   |
| llama    | no                 | con              | 2         | 36,42%    | 57,89%              | 45,63%          | 32,89%   | 36,42%   |
| llama    | no                 | sin              | 2         | 35,50%    | 57,57%              | 44,61%          | 31,19%   | 35,50%   |
| llama    | no                 | sacando B2       | 1         | 32,39%    | 53,17%              | 39,95%          | 31,18%   | 32,39%   |

Tabla 2: Los 10 mejores experimentos ordenados segun su accuracy aproximada.

### Discusión de los Resultados de Clasificación

**Comparación entre modelos entrenados y no entrenados**  
Los experimentos compararon el rendimiento de modelos preentrenados para clasificación (BERT-Ta y BERT-Ab) con los modelos de lenguaje general (Llama 3.1 y Orca 2). Llama 3.1 logró superar la accuracy de los modelos entrenados en algunos experimentos, destacándose como un modelo con potencial competitivo en tareas de clasificación CEFR sin necesidad de ajuste previo específico.

**Rendimiento del modelo Orca**  
Orca 2 presentó un rendimiento considerablemente inferior en accuracy en comparación con Llama 3.1 y los modelos preentrenados. Además, para ciertos prompts, Orca no lograba clasificar las muestras adecuadamente, resultando en un alto número de predicciones en la clase "unknown".

**Impacto de la configuración de shots**  
En el caso de Llama 3.1, se observó una mejora notable en accuracy al pasar de 0-shot a 1-shot, lo que evidencia el valor de proporcionar ejemplos explícitos en el prompt. Sin embargo, la mejora al pasar de 1-shot a 2-shot fue menor, indicando que aumentando la cantidad de ejemplos se obtienen mejoras decrecientes.

**Evaluación de prompts**  
- Prompts basados en criterios de enseñanza: A pesar de mostrar potencial durante la fase anecdótica, estos prompts no lograron resultados destacados en los experimentos formales.
- Prompts con descriptores de nivel: Consistentes con la exploración inicial, los prompts con descriptores fueron menos efectivos que los prompts mas simples.

**Mejores resultados**  
Los mejores experimentos se obtuvieron con prompts de 2-shot en Llama 3.1:  
41.65% accuracy: Prompt con lectocomprensión y corrección (excluyendo B2).  
39.54% accuracy: Prompt con lectocomprensión sin corrección.

Lectocomprensión resultó ser un factor positivo, ya que los prompts que incluían este enfoque superaron a los que no lo incluían.

Curiosamente, los prompts sin corrección general (excluyendo la estrategia de excluir B2) obtuvieron mejores resultados que aquellos con corrección explícita.

**Errores y distribución de predicciones**  
Las métricas accuracy pesada y accuracy aproximada se diseñaron para analizar la relación entre las predicciones y la etiqueta real en términos de distancia entre clases.

- Accuracy aproximada: Esta métrica recompensa las predicciones cercanas (distancia de 1) asignándoles un puntaje parcial de 0.5. Permitió diferenciar configuraciones con una accuracy modesta pero con un desempeño relativamente mejor en predicciones cercanas (por ejemplo, BERT-Ta).
- Accuracy pesada: Penaliza predicciones incorrectas en proporción a su distancia de la etiqueta real. Sin embargo, no logró diferenciar los experimentos de manera efectiva, manteniendo un orden de rendimiento similar al de la accuracy estándar. Las diferencias entre las métricas en dos experimentos eran escalables y proporcionales a sus valores de accuracy, limitando su utilidad práctica.

Estos hallazgos subrayan que la accuracy aproximada fue más informativa para identificar aproximaciones que, aunque no perfectas, lograron un mejor desempeño relativo en términos de cercanía entre las predicciones y las clases reales.

### Conclusiones de los Experimentos de Clasificación

**Modelo Orca**  
Se decidió no realizar más experimentos con Orca 2 debido a su baja performance. Su accuracy promedio fue del 20%, apenas superior al 16% esperado por una clasificación aleatoria, y significativamente menor al 29% alcanzado por Llama 3.1.

**Prompts con descriptores de nivel**  
Estos prompts mostraron un rendimiento inferior y, además, tienen un alto coste computacional. Por estos motivos, se descartaron para experimentos posteriores.

**Prompts con corrección de sesgos**  
Aunque el objetivo de la corrección era mitigar los sesgos observados en los modelos, los experimentos revelaron que los prompts sin corrección ofrecieron mejores resultados. Por ello, no se continuaron experimentos con este enfoque.

**Corrección excluyendo la clase B2**  
A pesar de que esta estrategia produjo el mejor resultado en 2-shot (accuracy de 41.65%), se decidió no continuar con ella debido a:
- Su carácter altamente ad-hoc y específico al conjunto de datos utilizado.
- La falta de evidencia de que este enfoque generalice bien a otros escenarios.
- La mejora obtenida respecto a otros prompts no justifica el sesgo introducido al excluir una categoría completa.

## Fase 2: Adaptación de Textos en nivel especifico de CEFR

### Introduccion
En esta sección se detallan los experimentos realizados para evaluar la capacidad de los modelos de lenguaje para adaptar textos a niveles CEFR específicos. Estos experimentos exploran cómo los modelos pueden transformar un texto original en versiones adecuadas para distintos niveles de competencia lingüística, manteniendo sentido, coherencia y adecuación al nivel deseado.

### Diseño de las Aproximaciones

**Objetivo**  
El objetivo fue analizar el desempeño de las aproximaciones en la adaptación de textos entre niveles CEFR, considerando tanto su capacidad para realizar estas transformaciones como la calidad del texto adaptado.

**Configuración de las Aproximaciones**  
Se llevaron a cabo dos aproximaciones 0-shot, con las siguientes configuraciones:
- Sin lectocomprensión
- Con lectocomprensión
  
Estos prompt son los mismos que se utilizaron en la parte de clasificación, pero que fueron adaptados para esta parte.

**Motivación de los enfoques 0-shot**  
Para realizar experimentos 1-shot y 2-shot, era necesario contar con ejemplos manuales de adaptación entre niveles (por ejemplo, de A1 a A2, A1 a B2, etc.).
Estos ejemplos debían ser creados por expertos en el dominio, quienes adaptarían textos de forma controlada y adecuada.
Sin embargo, no fue posible disponer de estos ejemplos a tiempo, por lo que los experimentos 0-shot fueron la única alternativa viable.

**Restricción en las adaptaciones por niveles**  
Se estableció un límite de dos niveles de diferencia máxima entre el nivel original y el nivel objetivo de adaptación. Esto significa:

- Un texto clasificado originalmente como A1 se adaptó a A1, A2 y B1.
- Un texto clasificado como B2 se adaptó a A2, B1, B2, C1 y C2.

Esta decisión se basó en una sugerencia por parte de TaskGen, ya que los profesores tienden a adaptar textos hacia niveles cercanos al original (uno o dos niveles por encima o por debajo), evitando distancias mayores, ya que estas tienden a afectar la coherencia y el sentido del texto adaptado.

**Estructura de los Experimentos**  
Cada uno de las aproximaciones se dividió en seis experimentos según el nivel objetivo de adaptación:
- Textos adaptables a A1.
- Textos adaptables a A2.
- Textos adaptables a B1.
- Textos adaptables a B2.
- Textos adaptables a C1.
- Textos adaptables a C2.
  
Esta clasificación permite analizar de manera específica el rendimiento del modelo para cada nivel CEFR, considerando tanto la complejidad de los textos originales como los desafíos inherentes a cada nivel objetivo de adaptación.  
Todos los prompts utilizados se encuentran en esta [planilla](https://github.com/juan-oviedo/Adaptacion-de-textos-para-aprendizaje-de-ingles-como-lengua-extranjera/blob/main/Experimentos/Experimentos%20Adaptacion.xlsx)

### Métricas de Evaluación en Adaptación de Textos

Dado que no se pudo realizar una evaluación directa por expertos en el dominio, se optó por utilizar métricas automáticas para evaluar de manera orientativa la calidad de las adaptaciones generadas por los modelos. Estas métricas permitieron analizar tanto la complejidad como la coherencia semántica de los textos adaptados en relación con los originales.

#### Métricas Utilizadas

**Flesch-Kincaid Grade Level (FKGL)**  
- Propósito:  
Evaluar la complejidad lingüística de los textos adaptados, midiendo la relación entre el nivel CEFR objetivo y la dificultad esperada de los textos.

- Metodología:   
Se calculó el FKGL de cada texto original y se agruparon los resultados por nivel CEFR original.  
Se calculó la media de FKGL para cada nivel, proporcionando un valor de referencia para las adaptaciones.  
Para los textos adaptados, se calculó el FKGL medio por experimento.  
Posteriormente, se calculó el error cuadrático entre el FKGL del nivel objetivo del experimento y el FKGL promedio de las adaptaciones.  
Finalmente, se sumaron los errores de todos los experimentos de cada aproximación para obtener un puntaje global de adecuación al nivel esperado.  

- Interpretación:  
Un menor error cuadrático indica que las adaptaciones son más consistentes con el nivel CEFR objetivo del DataSet.

**BERTScore**  
- Propósito:  
Evaluar la similitud semántica entre el texto original y el texto adaptado, asegurando que las adaptaciones mantengan el contenido esencial del texto original.

- Metodología:  
Se calculó el BERTScore para cada adaptación en términos de precisión, recall y F1.  
Se calculó la media de estas métricas por experimento.  
Finalmente, se promedió cada métrica a nivel de aproximación para obtener un resumen global del desempeño de los modelos.  

- Interpretación:  
Precisión alta: Indica que las adaptaciones conservan la mayoría de las palabras relevantes del texto original.  
Recall alto: Sugiere que las adaptaciones capturan la mayor parte del contenido semántico del texto original.  
F1: Balance entre precisión y recall, utilizado como métrica global para evaluar la similitud semántica.

### Resultados de Adaptación

A continuación, se presentan los resultados de los experimentos de adaptación, evaluados según las métricas de Flesch-Kincaid Grade Level (FKGL) y BERTScore (precisión, recall y F1). Los resultados incluyen la comparación entre los enfoques con y sin lectocomprensión.

**Resultados de FKGL**

| Clase | Original | Sin LectoComprensión | Con LectoComprensión |
|-------|----------|-----------------------|-----------------------|
| A1    | 1.276    | 1.367                | 1.508                |
| A2    | 3.807    | 2.247                | 2.546                |
| B1    | 7.613    | 5.872                | 5.634                |
| B2    | 9.793    | 11.437               | 10.669               |
| C1    | 12.103   | 14.740               | 14.167               |
| C2    | 14.876   | 16.165               | 15.362               |
| **Error Cuadrático** |          | 16.788                | 10.823               |

Tabla 3: resultados FKGL

**Resultados de BERTScore**

Precisión Promedio:

| Clase                     | Sin LectoComprensión | Con LectoComprensión |
|---------------------------|-----------------------|-----------------------|
| A1                        | 91.96%               | 91.51%               |
| A2                        | 92.11%               | 91.67%               |
| B1                        | 93.19%               | 92.10%               |
| B2                        | 91.82%               | 91.21%               |
| C1                        | 91.19%               | 90.75%               |
| C2                        | 90.76%               | 90.85%               |
| **Promedio por Aproximación** | 91.84%               | 91.35%               |

Tabla 4: BERTScore precisión promedio 

Recall Promedio:

| Clase                     | Sin LectoComprensión | Con LectoComprensión |
|---------------------------|-----------------------|-----------------------|
| A1                        | 89.25%               | 89.35%               |
| A2                        | 89.42%               | 89.53%               |
| B1                        | 92.10%               | 90.85%               |
| B2                        | 91.26%               | 90.23%               |
| C1                        | 91.13%               | 90.37%               |
| C2                        | 90.69%               | 90.43%               |
| **Promedio por Aproximación** | 90.64%               | 90.13%               |

Tabla 5: BERTScore recall promedio 

F1 Promedio:

| Clase                     | Sin LectoComprensión | Con LectoComprensión |
|---------------------------|-----------------------|-----------------------|
| A1                        | 90.58%               | 90.40%               |
| A2                        | 90.74%               | 90.58%               |
| B1                        | 92.63%               | 91.46%               |
| B2                        | 91.53%               | 90.71%               |
| C1                        | 91.15%               | 90.55%               |
| C2                        | 90.72%               | 90.64%               |
| **Promedio por Aproximación** | 91.23%               | 90.72%               |

Tabla 6: BERTScore F1 promedio 

### Discusión de los Resultados

**Flesch-Kincaid Grade Level (FKGL)**  
Los resultados de FKGL muestran una ventaja general para los prompts con lectocomprensión, especialmente en los niveles CEFR más altos (B2, C1, C2). Esto sugiere que los prompts con lectocomprensión logran adaptaciones más adecuadas en términos de complejidad textual para niveles avanzados.  
En contraste, los prompts sin lectocomprensión mostraron un mejor rendimiento en las clases inferiores (A1, A2, B1).

**BERTScore**  
En lo que respecta a BERTScore y sus métricas (precisión, recall y F1), los prompts sin lectocomprensión obtuvieron resultados ligeramente superiores. Sin embargo, la diferencia fue marginal en todos los casos, lo que indica que ambos enfoques mantienen una similitud semántica comparable entre los textos originales y los adaptados.

### Conclusión
Aunque las métricas empleadas no garantizan una evaluación completamente precisa para determinar la calidad de las adaptaciones de textos destinadas al aprendizaje de lenguas extranjeras, ofrecen una orientación general útil para comparar las distintas aproximaciones.  
Dado que los prompts con lectocomprensión obtuvieron un menor error cuadrático en FKGL, y que la diferencia en BERTScore entre ambas estrategias es marginal, se concluye que los prompts con lectocomprensión son la mejor aproximación para este objetivo.  
Un aspecto destacable de los resultados es que las adaptaciones realizadas con LLMs muestran potencial:
- FKGL indica que las adaptaciones logran mantener niveles de complejidad cercanos a los textos originales.
- BERTScore sugiere que las adaptaciones preservan adecuadamente el contenido semántico de los textos originales.
Estos resultados son prometedores, ya que demuestran que las adaptaciones generadas por LLMs pueden cumplir con criterios básicos de adecuación y fidelidad semántica, lo que constituye un buen punto de partida para futuras evaluaciones más rigurosas y supervisadas por expertos en el dominio.

## Conclusión General del Informe
Este informe detalla un análisis integral sobre el uso de modelos de lenguaje grande (LLMs) en dos tareas fundamentales: la clasificación de textos según niveles CEFR y la adaptación de textos para el aprendizaje de lenguas extranjeras. Obteniendo las siguientes conclusiones:

- Clasificación:  
Los experimentos demostraron que los LLMs, especialmente Llama 3.1, pueden ser una herramienta valiosa para clasificar textos según niveles CEFR. Sin embargo, la mejora en precisión y la minimización de errores en predicciones lejanas sigue siendo un área de oportunidad.

- Adaptación:  
Las adaptaciones automáticas de textos realizadas por los LLMs tienen un potencial significativo para su uso en entornos educativos. Aunque estas aproximaciones requieren validación por parte de expertos, los resultados sugieren que estas herramientas pueden servir como punto de partida para generar materiales adaptados.

- Impacto Educativo:  
Este trabajo demuestra que los LLMs pueden ser un recurso útil para tareas complejas relacionadas con el aprendizaje de lenguas, pero también subraya la importancia de una colaboración más estrecha con expertos humanos para mejorar la calidad y utilidad de los resultados.

- Perspectivas Futuras:  
Aunque las métricas utilizadas ofrecen una visión general confiable, futuras investigaciones deberían centrarse en incorporar evaluaciones cualitativas y en ampliar las pruebas con datasets más diversos y adaptaciones validadas por expertos. Además, sería valioso explorar técnicas de ajuste fino y optimización de prompts para maximizar el rendimiento de los LLMs en ambas tareas.

## Plan Futuro con Recursos
En caso de contar con un equipo de cinco personas trabajando a tiempo completo durante un año y un alto presupuesto, el proyecto evolucionaría significativamente, enfocándose en tres áreas principales: la creación de un dataset especializado, la evaluación cualitativa de las adaptaciones automáticas y el desarrollo de infraestructura y experimentación avanzada.

**1. Creación de un Dataset Especializado**  
La primera y más crucial tarea sería la construcción de un dataset de alta calidad que contenga textos originales y sus correspondientes adaptaciones a diferentes niveles CEFR. Para esto, se contratarían profesores de inglés con experiencia en la enseñanza de lenguas extranjeras, quienes se encargarían de:  
Generar adaptaciones manuales de textos para cubrir todas las combinaciones posibles de niveles (por ejemplo, A1 a A2, B2 a B1, etc.).  
Asegurarse de que las adaptaciones reflejen prácticas reales de enseñanza, respetando tanto la gramática como la adecuación cultural y lingüística de cada nivel.  
Este dataset sería una herramienta clave para realizar fine-tuning de modelos, permitiendo que los LLMs puedan especializarse en la tarea de adaptación de textos.  

**2. Evaluación Cualitativa y Métricas Humanas**  
Un equipo de profesores y expertos en didáctica del idioma inglés también se dedicaría a:  
Evaluar las adaptaciones automáticas generadas por los LLMs, identificando fortalezas y debilidades en comparación con las adaptaciones manuales.  
Diseñar y aplicar métricas cualitativas para complementar las métricas automáticas actuales, con el objetivo de capturar aspectos más subjetivos como la fluidez, adecuación y relevancia del contenido adaptado.

**3. Infraestructura y Experimentación Avanzada**  
Se invertiría en la creación de una infraestructura tecnológica robusta para realizar experimentos a gran escala. Esto incluiría:  
Servidores y GPUs de alto rendimiento, optimizados para tareas de procesamiento de lenguaje natural, con capacidad suficiente para ejecutar modelos grandes y realizar múltiples experimentos en paralelo.  
Desarrollo de pipelines automatizados para la evaluación de adaptaciones, simplificando el proceso de comparación entre diferentes configuraciones de prompts, niveles y modelos.

## Agradecimientos
Quiero expresar mi sincero agradecimiento a todas las personas e instituciones que hicieron posible el desarrollo de este proyecto:  
- **Laura Alonso Alemany**, docente a cargo de la materia, por su excelente guía durante el curso y por brindar reuniones de ayuda y seguimiento que resultaron clave para el avance y la finalización de este proyecto.

- **TaskGen**, el proyecto que inspiró las ideas centrales de este trabajo y a **Eli Comelles**, por el tiempo y apoyo a lo largo del proyecto.
 
- **Centro de Cómputos de Alto Desempeño (CCAD)** por proveer la infraestructura necesaria, permitiendo el uso de GPUs de alto rendimiento, fundamentales para la realización de los experimentos.
  
- **Easse**, la biblioteca que implementa métricas especializadas para la evaluación de lenguaje natural, cuyo aporte fue esencial para analizar los resultados de las adaptaciones.
