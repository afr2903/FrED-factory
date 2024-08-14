***Automatización de sistemas de manufactura (Gpo 602\)***

 

# Actividad Reto FRED Factory-2 Automatización de Estación de Trabajo XARM \- Video y Entrega Final \- competencia SMR0100 Integra (SMR0101, SMR0103, SMR0104)

**Dr. Erick Guadalupe Ramírez Cedillo**

**Sergio Siller Lobo              			| A00833806** 

**Jesus Fernando Davila              		| A01383355** 

**André Mauricio Mendoza Quevedo		| A01284836**

**Ángel Mario Alarcón López			| A00832669**

**Adán Flores Ramírez				| A01612331**

**Fecha de entrega:**

2 de Junio 2024


# **Introducción** {#introducción}

La Estación 2 desempeña un papel crítico en el funcionamiento integral del FrED, ya que se encarga de la electrónica fundamental de la máquina, que es esencial para su control y autonomía. Su tarea principal implica el ensamblaje preciso de componentes clave, incluyendo un Arduino Mega, un módulo de Shield Ramp 1.4 y dos drivers de motor A4988.

Ante el desafío de lograr una estación completamente automatizada para la producción de los FrEDs, se ha aceptado este reto con el objetivo de reducir el error humano y aumentar la eficiencia y constancia en las iteraciones del proceso. Esto se logra mediante operaciones de pick and place realizadas con un gripper personalizado, el cual cuenta con configuraciones variables que permiten manipular electrónicos de diversos tamaños de manera precisa y segura.

En las siguientes secciones, se explorarán en detalle cada aspecto del diseño de esta estación, incluyendo sus componentes, funciones específicas, y el funcionamiento coordinado de cada uno dentro del proceso de ensamblaje automatizado de los FrEDs.

![][image2]

*Figura 1\. a) Vista Explosionada del Ensamble , b) Bill of materials del Ensamble.*

1. # **Fundamentos y Aplicación Tecnológica para procesos Automáticos de Manufactura** {#fundamentos-y-aplicación-tecnológica-para-procesos-automáticos-de-manufactura}

   1. ## Impresión 3D y Corte Láser {#impresión-3d-y-corte-láser}

      1. ### *Piezas Fabricadas por Procesos Automáticos* {#piezas-fabricadas-por-procesos-automáticos}

#### Impresión 3D con PLA {#impresión-3d-con-pla}

La impresión 3D permite la creación de geometrías complejas y personalizadas que optimizan la funcionalidad de las piezas impresas. Se pueden diseñar estructuras internas específicas, como celdas de panal, que aumentan la resistencia y reducen el peso, mejorando así el rendimiento de las piezas.

* **Gripper:** El diseño del dispositivo utiliza un mecanismo de piñón y cremallera con dos divisiones, cada una con dedos de agarre para diferentes objetivos. La división principal, con dedos grandes, sujeta componentes grandes como el "shield" y la tarjeta Arduino. La segunda división, más pequeña, ensambla los drivers, permitiendo su colocación a presión. El mecanismo de piñón y cremallera permite extender los dedos a diferentes distancias, facilitando la manipulación eficiente de objetos de diversos tamaños.  
* **Caja para Electrónica:** El diseño de esta caja busca proteger toda la electrónica que permite el funcionamiento y alimentación del gripper por lo cual cuenta con un diseño sencillo pero a la vez eficaz para permitir su manipulación de una manera sencilla.  
* **Base de canal para Drivers:** Esta base cumple la función de restringir el movimiento de los Shield cuando uno es retirado para ensamblaje, y busca garantizar precisión en una acción de Pick.  
* **Base para Ensamblaje:** La base donde sucede el ensamblaje del Arduino con el Shield, busca precisamente imitar la forma de la base del Arduino Mega de la manera más precisa posible, este diseño busca restringir el movimiento del Arduino Mega cuando sea colocado y permite un ensamblaje correcto.  
* **Soporte de Indicadores:** El diseño de este soporte está hecho en 3 partes, la primera es la pinza que se encarga de soportar todos los Indicadores, la segunda parte es la caja donde pasan las conexiones y esconde los Indicadores, finalmente la tercera parte, es una tapa la cuál permite un manejo más sencillo de los Indicadores en un caso donde se tengan que hacer modificaciones.   
* **Soporte de Sensor:** Este es el diseño más sencillo de los anteriores, pero precisamente su sencillez es lo que nos ayuda a poder colocar el sensor en una posición cómoda y precisa para la detección del FrED.

#### Corte Laser con MDF {#corte-laser-con-mdf}

El uso de corte láser en MDF (Fibra de Densidad Media) ha demostrado ser una técnica eficaz para la fabricación de componentes precisos y consistentes en diversos proyectos.  
La precisión del corte asegura que todas las piezas se ajusten perfectamente, resultando en una base sólida y de alta calidad. Esto es crucial para la fabricación en serie, donde la uniformidad de las piezas es fundamental para la estabilidad y el ensamblaje correcto de las mesas.

* **Base de la mesa:** Diseño minimalista para la base la cuál sostendría todos los fixtures y bases donde se colocarían los elementos de la estación 2, al ser una base que busca cubrir la mayor superficie de la mesa, resulta más rentable realizarla con corte láser, más allá que imprimirla, debido a la poca complejidad de diseño de la misma.   
* **Caja de altura para base de ensamblaje:** Pequeña caja ensamblada con seis paredes de MDF para lograr darle altura a la base para ensamblaje y facilitar el ensamblaje al Robot.   
* **Rampas de Drivers, Arduino y Shield:** Diseño de rampas a precisión para cada uno de los componentes electrónicos a ensamblar 

![][image3]  
*Figura 2\. Piezas Fabricadas \- a) Gripper, b) Mesa Fixture, c) Sensor Fixture, d) Driver fixture, e) Shields fixture, f) Arduino fixture, g) Ensamble Fixture, h) Torreta.*

2. ### *Señalización de los Elementos de la Estación* {#señalización-de-los-elementos-de-la-estación}

La señalización de la estación se dividió en dos partes: seguridad e información. Para determinar las señales de seguridad necesarias, realizamos un análisis de riesgos (ver figura 2b). El principal riesgo identificado es la posible colisión entre el robot y el operario, que puede causar lesiones menores. Es importante señalar que el robot se mueve. También se especificaron los componentes eléctricos en movimiento, como el Arduino, el shield y los drivers. La señal más importante indica puntos de posible pinzamiento. Estas señales aseguran el cumplimiento de la normativa ISO/TS 15066 [\[4\]](\#bookmark=id.nabgplmgqtkv) para la seguridad en entornos de robots colaborativos.

Las señales informativas identifican qué fixture corresponde a cada componente electrónico, como el shield, el Arduino, FRED, y el fixture para el proceso de ensamblaje, facilitando las operaciones del robot.

![][image4]  
*Figura 3\. Señalización de la Estación  \- a) Visto Superior de la Estación Señalizada, b) Señalización de seguridad colocada.*

3. ### *Cableado y Sujeción de los Elementos* {#cableado-y-sujeción-de-los-elementos}

#### Cableado {#cableado}

El cableado de la estación fue gestionado y organizado con cinchos de plástico, estos facilitan la organización y restringen el espacio de movimiento de los cables (ver figura 4), de esta forma garantizamos una estación de trabajo eficiente y limpia.  
![][image5]  
*Figura 4 Organización del cableado*

#### Sujeción de Elementos {#sujeción-de-elementos}

Para la sujeción de los diferentes fixtures de la estación se utilizaron dos herramientas principales:

* **Resina:** La resina actúa como un adherente para el MDF, de esta forma logramos garantizar la sujeción de todos los fixtures al fixture de la mesa, y  poder garantizar exactitud y precisión al momento de hacer iteraciones.  
* **Tornillería:** El gripper fue ensamblado y montado con el uso de tornillería, de esta manera garantizamos robustez en el gripper y un montado efectivo al brazo robótico, además del gripper, también se utilizó tornillería para fijar la posición del fixture de la mesa, de esta manera se lograba poder montar y desmontar la estación sin dificultades. 

  4. ### *Implementación de la Metodología 5S* {#implementación-de-la-metodología-5s}

* **Clasificación:** Todos los elementos necesarios de la estación de trabajo se encuentran etiquetados de manera clara.  
* **Orden:** Todos los fixtures y elementos de la estación de trabajo cuentan con un lugar específico y definido, así como garantizamos la ubicación de los elementos más utilizados en áreas de fácil acceso para mejorar eficiencia.    
* **Limpieza:** La estación de trabajo no cuenta con elementos no necesarios, a su vez que se mantiene libre de polvo y residuos.   
* **Estandarización:** Se establecieron estándares de cómo se colocarían los fixtures de la electrónica, con ayuda de los indicadores se estandarizó las acciones que puede realizar el operador en cada color, se establecieron fechas de mantenimiento y pruebas a la estación para garantizar de esta manera que la estación de trabajo funcione de manera adecuada.  
* **Disciplina:** Mediante el trabajo en equipo, la involucración de cada uno de los miembros del equipo en el proyecto, representa un compromiso hacia el mismo y permite proyectar un interés hacia las demás personas. 

![][image6]  
*Figura 5\. Vista Superior de la Estación con 5S implementada.*

2. ## Robótica Colaborativa {#robótica-colaborativa}

   1. ### *Programación de Rutinas de Robot* {#programación-de-rutinas-de-robot}

El manejo de la rutina completa de automatización, incluyendo las posiciones del brazo robótico y la comunicación con el PLC, Gripper y Cámara, se controlan a través de un script de Python. Se decidió hacer de esta manera por la versatilidad y diversidad de funciones que ofrece este lenguaje de programación de alto nivel, a comparación con la aplicación de Blockly de uFactory.

#### Cálculo de TCPs {#cálculo-de-tcps}

Nuestro Gripper electrónico personalizado cuenta con dos grippers: uno para agarrar componentes grandes como el arduino y shield (BOARD), y el otro para componentes pequeños como los drivers (WIRE).  
Por unos días se utilizó sólo movimientos de tipo joint pues los lineales no funcionaban al no tener configurado el TCP. Finalmente decidimos calcular el TCP utilizando el método de 4 puntos, disponible en el software de uFactory.  
Para cada uno de los grippers, se calculó el TCP usando como referencia la esquina de un fixture de componentes, desde 4 posiciones diferentes, con el modo manual. Se obtuvieron los siguientes valores, que se introdujeron en el código:  
![][image7]  
*Figura 6\. TCP de ambos grippers.*

#### Posiciones del robot {#posiciones-del-robot}

Dentro de la clase principal del programa, se tiene un diccionario (lista) con todos los estados del robot dentro de la rutina. Cada una tiene un nombre representativo del movimiento a realizar y la posición objetivo. Posteriormente, se debe indicar la luz LED a encenderse con dicho estado, el tipo de movimiento (joint/lineal), cada una de las joints/coordenadas, la velocidad del movimiento, y de ser lineal, el TCP:  
![][image8]  
*Figura 7\. Posiciones del Robot.*

Debido a que son más de 40 posiciones ya que se optimizó por completo la estación, el resto de los estados del robot se pueden encontrar en el código (anexos): 

Se cuenta con bastantes posiciones de seguridad, entre las cuales están las que tienen el prefijo “SAFE”, “BEFORE” o “AFTER” en el nombre del estado.  
Para optimizar los tiempos de ciclo del movimiento, se ha incrementado la velocidad en los movimientos rápidos de tipo joint, y sólo se mantuvo velocidad lenta en los movimientos lineales de alta precisión. Se consiguió ser la estación con tiempo de ciclo más corto, de 2 minutos y medio aproximadamente.

#### Posiciones del gripper {#posiciones-del-gripper}

Al contar con un gripper electrónico personalizado, se requieren enviar posiciones de servomotor para cada gripper. Estas posiciones se encuentran guardadas en otro diccionario, con el mismo nombre que la posición del robot asociada. Se envían al microcontrolador del gripper vía UDP después de mover el robot:  
![][image9]  
*Figura 8\. Posiciones de los grippers*

Para ejecutar la posición y controlar al robot, se utiliza la siguiente función en Python, que identifica el tipo de movimiento deseado, y de ser lineal, cambia el TCP:  
![][image10]  
*Figura 9\. Controlador del TCP.*

#### Diagrama de trayectorias {#diagrama-de-trayectorias}

Ya que se tiene una gran cantidad de trayectorias, se ha generado una imagen animada (GIF) en cámara rápida con todos los movimientos realizados por el robot.

**![][image11]**

*Figura 10\. Diagrama de trayectorias. ([diagrama\_trayectorias.gif](https://drive.google.com/file/d/1DX9Bfj2y6WRKWcEhGp6MrHlwTN5V51MT/view?usp=sharing))*

2. # **Diseño de Interfaces SCADA** {#diseño-de-interfaces-scada}

   1. ## Supervisión, Control y Reconfiguración de Celdas de Manufactura Automatizadas {#supervisión,-control-y-reconfiguración-de-celdas-de-manufactura-automatizadas}

      1. ### *Diagrama de Conexiones y Comunicación* {#diagrama-de-conexiones-y-comunicación}

En este diagrama se muestran las conexiones eléctricas y el tipo de comunicación entre los diferentes dispositivos, sensores y actuadores.  

![][image12]  
*Figura 11\. a) Diagrama general de conexiones eléctricas y de comunicación de dispositivos, b)Diagrama de conexiones enfocado a PLC y CBX100, c)Simbología de diagrama de conexiones.*

Finalmente se tiene el diagrama del “Circuito G”, el cual representa el circuito utilizado para el gripper. Muestra sus conexiones eléctricas con el convertidor de voltaje tipo “Buck” de 24v y comunicación del ESP32 a través de bluetooth.  
![][image13]  
*Figura 12\. Diagrama de conexiones enfocado al circuito utilizado para el gripper electrónico.*

2. ### *Uso de Sensores* {#uso-de-sensores}

La estación cuenta con un sensor de presencia infrarrojo el cuál se utilizó para la detección de la presencia o ausencia del FrED en el espacio de trabajo, de esta manera garantizar que sí se inicia la rutina de ensamble solamente se haga sí el sensor detecta la presencia del FrED. 

3. ### *Uso de Actuadores* {#uso-de-actuadores}

La estación incluye 2 actuadores en la forma de servomotores, estos son utilizados para controlar la apertura del gripper diseñado. Se escogieron estos servos por su ligero peso, y a su vez alta fuerza de torque. Al utilizar un gripper electrónico garantizamos el control de las aperturas del gripper, para poder realizar acciones de Pick and Place, y empuje, logrando un proceso completamente automatizado.

4. ### *Uso de Indicadores* {#uso-de-indicadores}

Los indicadores utilizados en la estación son del tipo LED Industrial, y se utilizan 3 de estos, un indicador de color verde, uno de color ambar y uno rojo, en ese orden respectivamente. La función que cumplen estos indicadores es representar mediante un esquema de colores las etapas del proceso en los que el operador puede acceder en la zona de trabajo de manera libre (verde), puede acceder en la zona de trabajo con precaución (ámbar), y no puede acceder a la zona de trabajo (rojo). 

3. # **Aplicación de la Tecnología de Grupos para el Diseño de SMA** {#aplicación-de-la-tecnología-de-grupos-para-el-diseño-de-sma}

   1. ## Eliminación de Tiempos Muertos {#eliminación-de-tiempos-muertos}

      1. ### *Estrategias de Automatización* {#estrategias-de-automatización}

Al tener una estación completamente automatizada, el árbol de operaciones y la secuencia de operaciones, sólo incluye movimientos del robot, por lo que no pueden existir tiempos muertos. Las únicas pausas suceden para abrir el gripper, lo cuál debe hacerse cuando el robot se encuentra detenido al llegar a una posición.  
La funcionalidad extra que agregamos de emitir retroalimentación con voz, fue programada para suceder a la par de ciertos movimientos del robot, utilizando la librería de **threading** de Python para correr tareas en paralelo:  
![][image14]  
*Figura 13\. Retroalimentación con voz*

![][image15]  
	*Figura 14\. a) Diagrama de secuencia , b) proceso de ensamblado.*

2. ## Diagrama de Conexiones {#diagrama-de-conexiones}

   1. ### *Componentes del Diagrama de Conexiones* {#componentes-del-diagrama-de-conexiones}

![][image12]  
*Figura 15\. a) Diagrama general de conexiones eléctricas y de comunicación de dispositivos, b)Diagrama de conexiones enfocado a PLC y CBX100, c)Simbología de diagrama de conexiones.*  
   

3. ## Comunicación de PLCs/PACs con Máquinas Automáticas {#comunicación-de-plcs/pacs-con-máquinas-automáticas}

   1. ### *Programación del PLC* {#programación-del-plc}

La programación del PLC en la estación 2, fue hecho principalmente como un medio de comunicación entre nuestro Script de python y los elementos electrónicos, mediante el uso de Data Blocks, se creó una línea de comunicación, de tal manera que pudiéramos controlar las señales del sensor infrarrojo y las señales de los indicadores de luz como se puede observar en la figura 16\.   
![][image16]  
*Figura 16\. Diagrama escalera PLC*

Como se mencionó anteriormente, el script de Python maneja toda la automatización de la estación, por lo que debe establecer una conexión al PLC mediante la librería de **snap7**, para poder acceder a los data blocks:  
![][image17]  
*Figura 17\. Código de comunicación de data blocks.*

El primer uso del PLC en la ejecución del programa, ocurre cuando se espera la señal del sensor. En el estado de “WAIT\_SENSOR”, se espera a recibir una lectura positiva de dicho sensor. Después se espera un tiempo determinado para que el operador libere el área de trabajo del robot, y vuelve a validar que no haya sido una lectura falsa. Si se vuelve a detectar el sensor, entonces se comienza la operación del brazo, hasta que quede ensamblado el FrED:  
![][image18]  
*Figura 18\. Lectura de sensor comunicada mediante snap7 para comparar con operadores lógicos.*

Para cada posición del brazo, va asociado un indicador LED que representa el [estado de la operación.](\#diseño-de-interfaces-scada) Este valor del LED también es enviado por data blocks para que el PLC pueda encender el indicador apropiado para el movimiento:  
![][image19]  
*Figura 19\. Código ciclos if de valores de luces comunicado mediante data blocks..*

4. ## Integración de Sistemas de Visión, Robots y PLCs/PACs {#integración-de-sistemas-de-visión,-robots-y-plcs/pacs}

   1. ### *Estrategia de Inspección con Cámara Datalogic* {#estrategia-de-inspección-con-cámara-datalogic}

La estrategia de inspección utilizada para la verificación de un ensamble correcto de la electrónica del FrED, se utiliza la herramienta “pinpoint pattern” el cuál utiliza una región de entrenamiento para crear un patrón (o modelo) a partir de una parte de una imagen. Cuando la herramienta se ejecuta, utiliza rutinas de correlación y coincidencia de contornos para encontrar una o más coincidencias con el patrón entrenado. Luego, calcula las puntuaciones de mejor coincidencia y proporciona esas puntuaciones y las coordenadas x-y de los patrones encontrados como una o más salidas de origen.  
En nuestro modelo, se entrenó la imagen para que esta pudiera detectar cuando ambos drivers se encuentran ensamblados de manera correcta en el Shield (ver Figura 24a) o en caso de que se encontrará mal ensamblado o no estuviera en posición la inspección fallaría (ver Figura 24b).

![][image20]  
*Figura 20\. Entrenamiento de cámara Datalogic en software VPM light.*

Dentro de la ejecución principal del código, en el estado de “INSPECTION” se envía una señal a una salida digital del brazo que se encuentra conectada al trigger de la cámara. Posteriormente, se obtienen los resultados de la inspección conectándose a la dirección IP de la cámara mediante la librería de **socket** de Python. La respuesta se convierte a un entero, y se da feedback por voz del resultado:  
![][image21]  
*Figura 21\. Código de estado de inspección de cámara.*

5. ## Programación del HMI y Automatización Completa {#programación-del-hmi-y-automatización-completa}

   1. ### *Programación del HMI* {#programación-del-hmi}

El diseño del layout para el HMI busca representar de manera gráfica y sencilla los cuatro aspectos principales de la estación a monitorear (ver figura 26).

1. **Cantidad de FrEDs fabricados (esquina superior izquierda)**: Este contador se controla mediante datablocks de tipo "Int" y aumenta cuando un FrED pasa satisfactoriamente la etapa de inspección.  
2. **Etapa de inspección (esquina superior derecha)**: En esta sección, un indicador luminoso se enciende según el resultado de la inspección realizada por la cámara. Esto se controla mediante un datablock del tipo "bool", ya que solo necesitamos saber si la inspección fue aprobada o no.  
3. **Cantidad de inventario disponible (esquina inferior izquierda)**: Similar al contador de FrEDs ensamblados, este contador monitorea la cantidad de inventario restante. El valor cambia cada vez que se retira un componente electrónico del inventario.  
4. **Presencia del FrED en la estación (esquina inferior derecha)**: Este aspecto indica si un FrED está presente en la estación, lo que ayuda a determinar si se debe realizar alguna operación. Además, se implementó un sistema de seguridad que requiere que el sensor infrarrojo detecte una señal constante durante más de 3 segundos antes de iniciar el proceso de ensamblaje. Esto previene accidentes por la colocación accidental de otros objetos frente al sensor.

![][image22]  
*Figura 22\. Pantalla de HMI.*

Para la vinculación con el código de Python, en la inicialización del programa se declararon variables con la cantidad inicial de inventario de cada componente:  
![][image23]  
*Figura 23\. Variables de inventario para HMI.*

Dentro de los estados de ejecución, se modifican los contadores después de las acciones de “PICK”. El valor actualizado se envía codificado a los bits del datablock correspondientes. El cambio en el inventario se verá reflejado en el HMI.  
![][image24]  
*Figura 24\. Comunicación de los estados de movimiento mediante data blocks.*

2. ### *Automatización Completa* {#automatización-completa}

El proceso de ensamblaje completamente automatizado de la estación se decidió manejar con un script de Python, gracias a la versatilidad y flexibilidad de este lenguaje. Dicha programación fue diseñada para ser modular, escalable y fácilmente entendible por personas sin estudios en Ciencias y Tecnologías Computacionales, manteniendo a la vez sus principios fundamentales. El script se encarga de ejecutar la rutina completa, incluyendo los movimientos del brazo robótico, las acciones del gripper personalizado y la comunicación con los periféricos (PLC, HMI, cámara).

#### Estructura del Software {#estructura-del-software}

El script sigue una estructura de Programación Orientada a Objetos, con la clase ElectronicsStation como núcleo. Esta clase encapsula el estado actual y el comportamiento de la estación, facilitando la gestión de la interacción entre los diferentes componentes.

* **Manejo de Estados:** El proceso de ensamblaje se divide en estados discretos (por ejemplo, HOME, PICK\_ARDUINO, INSPECTION), representados por diccionarios que mapean estos estados a acciones específicas. Este enfoque mejora la claridad y el mantenimiento del código, siendo fácil de editar.  
* **Funciones para Acciones:** El script define funciones como send\_gripper\_state y send\_arm\_state para encapsular la lógica de control del gripper y el brazo, respectivamente. Esto promueve la reutilización y legibilidad del código.  
* **Protocolos de Comunicación:** El script se comunica con el PLC utilizando la librería *Snap7* y con el gripper a través de *sockets* UDP. Estos mecanismos de comunicación se manejan dentro de la clase ElectronicsStation, manteniendo el código organizado.

#### Escalabilidad y Legibilidad {#escalabilidad-y-legibilidad}

El diseño del script favorece la escalabilidad. Si se agregan componentes o funcionalidades adicionales en el futuro, pueden integrarse en la estructura existente definiendo nuevos estados y acciones. Esto minimiza la alteración del código base existente. El programa prioriza la legibilidad:

* **Comentarios:** Se incluyen comentarios claros en todo el código para explicar el propósito de cada sección y variable, lo que facilita la comprensión para quien no está familiarizado con Python.  
* **Nombres Descriptivos:** Las variables y funciones tienen nombres autoexplicativos (por ejemplo, arduino\_counter, speech\_feedback), lo que mejora aún más la comprensión del código.  
* **Funciones Modulares:** Al dividir el código en funciones más pequeñas y bien definidas, el script se vuelve más fácil de depurar y modificar.

#### Funcionalidades Clave {#funcionalidades-clave}

Algunas de las funcionalidades principales del script son:

* **Retroalimentación por Voz (speech\_feedback):** El script utiliza indicaciones de voz generada por computadora para informar al operador sobre el estado actual, mejorando la experiencia del usuario.  
* **Control del Gripper (send\_gripper\_state):** Se logran movimientos precisos del gripper enviando comandos de posición de los servomotores, a través de Wifi UDP a un microcontrolador ESP32.  
* **Intercambio de Datos con el PLC:** El script intercambia datos con el PLC, actualizando contadores, recibiendo activaciones de sensores y controlando luces para sincronizar el proceso de ensamblaje con el entorno de producción más amplio.  
* **Calibración Semiautomática (record\_state):** El script incluye un modo para registrar nuevas posiciones del brazo y del gripper, simplificando el proceso de calibración para los técnicos.  
* **Manejo de Errores (handle\_err\_warn\_changed):** El script maneja los errores de manera eficiente, registrándolos y finalizando la ejecución para evitar daños al sistema.

#### Importancia de las Buenas Prácticas de Software en la Automatización {#importancia-de-las-buenas-prácticas-de-software-en-la-automatización}

La ingeniería de software sólida es fundamental para los sistemas automatizados. Un código bien estructurado, escalable y mantenible garantiza que la estación de electrónica pueda adaptarse a cambios futuros, reduciendo el tiempo de inactividad causado por errores y en consecuencia, mejorando la eficiencia y fiabilidad general del proceso de producción. Al aplicar buenas prácticas de software, no solo se construye una mejor estación de electrónica, sino también un sistema de fabricación más flexible y resiliente.

4. # **Elementos de un Sistema Automatizado de Manufactura y sus Niveles** {#elementos-de-un-sistema-automatizado-de-manufactura-y-sus-niveles}

   1. ## Diagramas y Clasificación {#diagramas-y-clasificación}

      1. ### *Diagrama de Elementos y Niveles de Automatización* {#diagrama-de-elementos-y-niveles-de-automatización}

![][image25]  
Figura 25\. Diagrama de Niveles de Automatización

2. ## Gripper y Fixtures {#gripper-y-fixtures}

   1. ### *Gripper para el Robot* {#gripper-para-el-robot}

#### Diseño y funcionamiento del Gripper {#diseño-y-funcionamiento-del-gripper}

El diseño del dispositivo se basa en un mecanismo de piñón y cremallera. Este consta de dos divisiones, cada una con sus propios dedos de agarre. Ambos emplean el mismo mecanismo, pero están destinados a objetivos diferentes. El dispositivo principal, equipado con dedos más grandes, se utiliza para sujetar componentes de circuitos más grandes, como el "shield" y el Arduino. Por otro lado, el segundo, de tamaño más reducido, se emplea para ensamblar los drivers. La elección del mecanismo de piñón y cremallera se debe a su capacidad para extender los dedos a diferentes distancias, lo que nos permite manipular objetos de diversos tamaños de manera eficiente.

#### Electrónica del gripper  {#electrónica-del-gripper}

Para controlar estos dispositivos, se ha diseñado un sistema basado en un microcontrolador ESP32, el cual dirige los movimientos mediante dos servomotores. Esta configuración proporciona un control preciso y confiable sobre el funcionamiento del dispositivo, garantizando una manipulación segura y efectiva de los componentes.

Siguiendo con el objetivo del gripper de proporcionar configuraciones dinámicas de pick y place, tanto para los electrónicos grandes como para los pequeños, se utilizaron dos servomotores **PDI-6225MG-300**.

Para obtener la alimentación necesaria, se encontró que el efector final del xArm 6 tiene un conector de 12 pines (ver Figura 26\) del cual se pueden sincronizar salidas digitales y voltaje nominal de 24V, en el manual de usuario de uFactory se pueden observar más detalles:

![][image26]

*Figura 26\. Datasheet xArm6 \- Conexión 12 pins* [\[1\]*.*](\#bookmark=kix.oi8uqhfeg8wa)

Dado que la alimentación lógica de nuestros componentes es de 5V, se utilizará un regulador de voltaje tipo “Buck converter” (ver Figura 27\) debido a su modularidad y facilidad de variar el valor del voltaje de entrada. En caso de fallos en las conexiones se quemaría el regulador, protegiendo así a los servomotores que son más costosos y difíciles de conseguir.

![][image27]

*Figura 27\. Buck converter* [\[2\]*.*](\#bookmark=kix.jwrwtufm0eta)

Durante las pruebas físicas, nos encontramos ante un problema mayor al plantear el funcionamiento a futuro. Para poder enviar información al gripper sobre qué posición es la deseada, había dos alternativas las cuáles implicarían un mayor número de conexiones y reguladores de voltaje:

* Conectar 4 salidas digitales: Ya sea desde el PLC o del efector final del brazo, necesitaríamos como mínimo una salida digital para cada una de las posiciones deseadas del gripper, para indicar qué electrónico se desea tomar.  
* Comunicación Serial: Desde las conexiones del controlador del brazo, se podía investigar cómo comunicarse por serial hacia los pines RX y TX del arduino, y de esta manera enviar y recibir datos.

Ambas alternativas requerirían bastante investigación y pruebas, y existía el riesgo de fallo que podría comprometer los electrónicos ya que se estaría trabajando con varias salidas de 24V.

Finalmente, se optó por una solución diferente y más simple, pues el Arduino Nano es un microcontrolador un poco más limitado en sus capacidades. En cambio, utilizar un ESP32 nos ofrecía una opción accesible y con la característica de esta familia que es su puerto UDP para ser utilizado mediante redes de internet.

De esta manera, sólo hay que proveer la alimentación de 5V y preconfigurar una red local de internet. Al momento de la ejecución del programa del xArm en Python, se podrá enviar la posición deseada al ESP32 (ver Figura 28\) mediante la librería de *socket*. Esta integración simplifica las conexiones electrónicas y brinda una implementación del Internet de las Cosas a este proyecto cuya filosofía es integrar tecnologías novedosas a un bajo costo.

![][image28]

*Figura 28\. Microcontrolador ESP32* [\[3\]*.*](\#bookmark=kix.rc5e3cqvhu5n)

#### Programación del Gripper {#programación-del-gripper}

El microcontrolador del gripper es un ESP32, que se programa de la misma manera que los Arduinos, la diferencia son algunas librerías que no son compatibles. La primera sección del programa, es la apertura de un canal de WifiUdp. Se declaran los objetos de los servomotores, y se inicializa todo.  
![][image29]  
*Figura 29\. Código de comunicación a ESP32 mediante Wifi Udp para estados de gripper.*

De manera continua, el código del ESP32 espera la llegada de datos mediante dispositivos conectados a su IP. La convención para los comandos posibles para recibir es (b/w)(grados del servomotor). Por ejemplo, si se quiere que el gripper grande (board), vaya a 31 grados, el comando esperado sería “b31”, o si se quiere que el gripper pequeño (wire) vaya 64 grados, se esperaría “w64”.  
![][image30]  
*Figura 30\. Código de estados para gripper.*

De manera local, el gripper almacena la posición actual en la variable, y se mueve a velocidad de 1 grado cada 20 segundos hasta llegar a la posición deseada.  
![][image31]  
*Figura 31\. Código para control de velocidad para abrir o cerrar gripper.*

2. ### *Fixtures necesarios* {#fixtures-necesarios}

1) #### Arduino Fixture {#arduino-fixture}

Diseño con pendiente permite que el peso de los componentes se desplace por la rampa y ocupe el lugar del componente recién tomado por el robot. Esto se traduce en que el robot necesite realizar la menor cantidad de trayectorias posibles para completar el ensamblaje de los FRED. El material que se usó para construir este Fixture fue MDF de 6mm. 

2) #### Shield Fixture {#shield-fixture}

El diseño del fixture para el shield sigue la misma filosofía que se utilizó para el fixture del Arduino, siendo prácticamente idénticos en su concepción (ver Figura 12). La principal diferencia radica en las dimensiones, ya que el fixture del shield es ligeramente más amplio para acomodar las dimensiones propias del shield, que son mayores que las del Arduino. Además, al seleccionar un fixture de este estilo, se consideraron varios factores importantes.

3) #### Driver A4988 Fixture {#driver-a4988-fixture}

Este fixture se desarrolló siguiendo la misma línea de diseño que los fixtures tanto para el Shield como para el Arduino. Se optó por dividir este fixture en dos partes: una parte fabricada con PLA para lograr una mayor precisión y otra parte de MDF para proporcionar la pendiente necesaria (ver Figura 13c). Esto se hizo para abordar el desafío específico presentado por los pines de conexión en la parte inferior del driver, los cuales tendían a atascarse entre las líneas de filamento.

4) #### Mesa Fixture {#mesa-fixture}

El diseño del fixture para la mesa cumple la función crucial de asegurar la estabilidad y fijación de todos los otros fixtures creados (ver Figura 14). Su propósito principal es mantener en su lugar los componentes durante el proceso de ensamblaje o trabajo. Esta solidez y estabilidad son fundamentales para garantizar la precisión y la eficiencia en la ejecución de las tareas, ya que evita movimientos no deseados o deslizamientos que podrían afectar la calidad del trabajo realizado.

5) #### Ensamble Fixture  {#ensamble-fixture}

El diseño del fixture para el ensamblaje busca imitar la forma del Arduino Mega, con el propósito de permitir la adición y el ensamblaje de todos los componentes de manera eficiente (ver Figura 16). Esta estrategia de diseño se basa en la idea de crear una plataforma que se adapte perfectamente a la geometría del Arduino Mega, proporcionando así un espacio de trabajo optimizado y ergonómico para la colocación y el montaje de los componentes, tales como el arduino, el shield ramp, los drivers y los cables. A este ensamble se le agregó una caja (ver Figura 17\) para darle altura para así no tener el proceso del ensamblado al límite del alcance del robot ya que nos encontrábamos con múltiples singularidades cuando se intentaba hacer dichas operaciones.

*![][image32]*

*Figura 32\. Fixtures del ensamble \- a)Arduino Diseño 3D, b) Arduino Diseño físico, c)Shield Diseño 3D, d) Shield Diseño físico, e) Driver Diseño 3D, f) Driver Diseño físico, g) Driver Ensamble rampa \- fixture, h) Mesa Diseño 3D, i) Mesa Diseño físico, j) Ensamble Diseño 3D, k) Ensamble Diseño físico, l) Caja de altura ensamble 3D.*

3. ### *Planos de los Fixtures, BOM y Explosión* {#planos-de-los-fixtures,-bom-y-explosión}

Nuestro layout fue actualizado a medida de que se realizaron correcciones para evitar colisiones y tener las piezas al alcance del “Workspace” del robot. Al final con la última versión de la estación esta fue mostrada y compartida con el encargado de grupo para agregarse al gemelo digital de la línea de producción.   
![][image33]  
*Figura 33\. BOM y Vista de Explosión* 

[***Lista dibujos técnicos (Anexo).***](https://docs.google.com/document/d/1yGBxXpGbBLFiIsMJwl6oGnlVT-DszvczajvD9J3PHRc/edit\#heading=h.gdlwsfu71dlp)

***1\. Dibujo técnico de acople.** \- Esta pieza une al gripper con el brazo robot x-arm.*  
***2\. Dibujo técnico de “Body”.** \-Esta pieza es el cuerpo principal del gripper, principalmente llevando el motor de los dedos grandes y los agujeros para la unión del cuerpo del pequeño gripper.*  
***3\. Dibujo técnico de dedo de gripper grande.** \- Dedos que actúan como pinzas y cuentan con una cremallera para su movimiento lineal.*  
***4\. Dibujo técnico de engrane grande.**\- Engrane para transmisión de torque del motor para dedos grandes.*  
***5\. Dibujo técnico de housing para motor de gripper chico.**\- Esta pieza cubre al servomotor para los dedos pequeños, contando con agujeros para acoplarse con tornillos al “body” y también colocar la base del gripper chico.*  
***6\. Dibujo técnico de base para gripper chico.**\- Esta pieza se coloca para detener el piñón del gripper chico y guiar las cremalleras individuales de los dedos pequeños.*   
***7.Dibujo técnico de cremallera de gripper chico.**\-Esta pieza se une con los dedos pequeños mediante dos tornillos a través de la ranura de la base del gripper pequeño.*  
***8.Dibujo técnico de dedo chico (variante 2).**\- Nuevos dedos pequeños para componente de menor tamaño con una menor longitud, para mayot torque.*  
***9.Dibujo técnico de piñón de gripper chico.**\- Engrane para transmisión de torque del motor para dedos pequeños.*  
***10\. Dibujo técnico fixture del arduino.***  
***11.Dibujo técnico base del fixture del arduino.***  
***12.Dibujo técnico pared del fixture del arduino.***  
***13.Dibujo técnico pared de atrás del fixture del arduino.***  
***14.Dibujo técnico rampa del fixture del arduino.***  
***15\. Plano de ensamble Shield Fixture***  
***16.Dibujo técnico base del fixture del Shield***  
***17.Dibujo técnico pared del fixture del Shield***  
***18.Dibujo técnico pared de atrás del fixture del Shield***  
***19.Dibujo técnico rampa del fixture del Shield***  
***20.Plano del fixture para el driver A4988.***  
***21.Dibujo técnico base del fixture del driver.***  
***22.Dibujo técnico de pared atrás del fixture del driver.***  
***23.Dibujo técnico de pared del fixture del driver.***  
***24.Dibujo técnico rampa del fixture del driver.***  
***25\. Dibujo técnico fixture final driver.***  
***26.Plano del fixture para la mesa.***  
***28.Plano del fixture para el ensamblaje.***

3. ## Workspace del Robot y del Operador {#workspace-del-robot-y-del-operador}

   1. ### *Diseño del Workspace* {#diseño-del-workspace}

El Workspace se diseñó de manera que las piezas a ensamblar siempre estén en la misma coordenada, permitiendo una automatización más eficaz, rápida y cómoda para el alcance del robot. El layout se desarrolló considerando el alcance del robot y el diseño del gripper, con el fin de evitar colisiones.

Además, el layout incorpora medidas de seguridad para el operador, incluyendo señalamientos de peligro y una torreta. Se aseguró también que los movimientos del robot no excedan los límites de la mesa para proteger al operador.

![][image34]  
*Figura 34\. Vista Superior Acotadas del Workspace*

5. # **Metodologías para la Modelación de Sistemas de Manufactura** {#metodologías-para-la-modelación-de-sistemas-de-manufactura}

   1. ## Gemelo Digital {#gemelo-digital}

      1. ### *Presentación del Gemelo Digital* {#presentación-del-gemelo-digital}

Se elaboró un gemelo digital en Process Simulate, este incluye todas las operaciones de la estación real, si bien las trayectorias del robot no son idénticas debido a limitaciones del software, se respetan tiempos y se asegura de que no haya colisiones con la estación, esto se logra a través de la inclusión de varias posiciones intermedias entre punto y punto para asegurarse de que el brazo tome una ruta deseada, ya que el software tiene a hacer que el brazo haga trayectorias con muchas colisiones. Asimismo el gemelo digital está disponible para verse en realidad virtual con un headset HTC VIVE, en este entorno el espectador puede caminar, acercarse y ver el proceso de la estación como guste.  
![][image35]  
*Figura 35\. a,e) Operador dejando el FRED en su fixture, b,f) Shield y arduino ensamblado en su fixture, c,g) Ensamble puesto en su fixture sobre el FRED, d,h) Operador llevándose el FRED a la siguiente estación*

*![][image36]*  
*Figura 36\. Demostración del gemelo digital en realidad virtual*

*Enlace a vídeo: [estacion2 FRED Factory Simulation](https://youtu.be/LHuBjLI-LG8?si=h2BF6kiicA4Vn7Os)*

2. ### *Colaboración en el Laboratorio* {#colaboración-en-el-laboratorio}

Metodología:  
El equipo se dividió por tareas con sus respectivos encargados, mientras unos diseñan y manufacturaban el gripper, otros estaban viendo la programación del robot, plc, hmi, otros diseñaron fixtures, etc. Si bien el trabajo fue dividido, siempre se mantuvo amplia comunicación entre todos para la contribución de ideas y ajustes a lo largo del desarrollo del proyecto. También establecimos varios deadlines para las diferentes etapas del proyecto, como lo fue tener listo el gripper, fixtures, rutina de automatización, etc. esto para no atrasarnos y no perder el ritmo de trabajo.

Para poder llevar a cabo este proyecto se utilizó la herramienta web Github, con la cuál podíamos además de respaldar y documentar todos nuestros códigos, hicimos uso de sus herramientas de project management para poder dar un seguimiento continuo al trabajo realizado, el primer paso fue dividir los roles del trabajo, a partir de un consenso grupal se decidió a un líder de equipo, este es el encargado de darle seguimiento a las tareas de manera individual y grupal, además se asignaron roles de Diseño CAD, Manufactura, Programación, Electrónica, la asignación fue la siguiente:

* **Lider de Equipo:** Ángel Alarcón  
* **Diseño CAD:** Sergio Siller, André Mendoza, Jesús Dávila  
* **Programación:** Adan Flores, Ángel Alarcón  
* **Electrónica:** Adan Flores, Ángel Alarcón  
* **Manufactura 3D:** Sergio Siller  
* **Manufactura Corte Laser:** Jesús Dávila

Una vez asignados los roles, se creó un diagrama de Gantt con el cuál pudiéramos darle seguimiento y actualizar las tareas, de tal manera que pudiéramos visualizar que se tiene que hacer, que ya se hizo, y cuánto tiempo tenemos para hacerlo (ver Figura 37).  
![][image37]  
*Figura 37\. Diagrama Gantt \- a) Gantt, b) Backlog* 

En nuestra experiencia dentro del laboratorio, se vivió un ambiente de gran apoyo y colaboración. Las diferentes estaciones se apoyaron mutuamente en múltiples formas, ya sea compartiendo habilidades, herramientas o conocimientos. En nuestro equipo, la experiencia fue muy positiva; todos trabajamos organizadamente, aprovechando nuestras mejores habilidades, con cada miembro encargado de las áreas donde se destacaba más.  
Aunque a lo largo del proyecto surgieron momentos de discusión o desacuerdo, tanto dentro de nuestra estación como con otras estaciones del salón, estos problemas siempre se mantuvieron como menores. Logramos llegar a acuerdos en los que ambas partes se beneficiaron. En cuanto al trabajo en equipo dentro de la estación, asignamos tareas basándonos en las cualidades de cada miembro, ya fuera diseño, programación o manufactura. Todos los problemas que surgieron se resolvieron mediante el diálogo, y siempre se tomó la decisión que más favoreció el resultado del proyecto.

2. ## Modelación de Planta y Procesos {#modelación-de-planta-y-procesos}

   1. ### *Diagrama de Operaciones de Procesos (DOP) y Diagrama de Recorridos* {#diagrama-de-operaciones-de-procesos-(dop)-y-diagrama-de-recorridos}

En el diagrama de operaciones podemos ver un flujo más sencillo gracias al nivel de automatización de la estación. Al no contar con tareas repetitivas para el operador no se encuentra un desperdicio de este, ya que no se necesita de un operador. Esto también nos ayuda a evitar tiempos muertos con un operador esperando tareas por realizar.   
![][image38]  
*Figura 38\. Diagrama DOP \- a) Parte 1, b) Parte 2* 

En el siguiente diagrama de recorrido se visualiza donde se realizan cada una de las operaciones dentro del layout.   
![][image39]  
*Figura 38\. Diagrama de recorrido sobre imagen real de layout.*

2. ### *Fabricación y Documentación de FrEDs* {#fabricación-y-documentación-de-freds}

La estación ensambla los componentes eléctricos principales del FRED, recibiendo la estructura base de la primera estación, nos encargamos de colocar el ensamble que incluye un arduino con un shield y 2 drivers de motor montados. Estos shields han sido modificados cambiando varias de sus terminales para así poder usar una fuente de poder externa que simplifica el cableado. El recorrido que hace el operador simplemente es recibir el FRED de la estación 1, camina hasta la estación 2, coloca este sobre su fixture, y la rutina inicia por su cuenta, al final, el operador toma el FRED y lo lleva a la siguiente estación.

Tiempos de ensayo (5 corridas seguidas \- MM:SS:MSMS):

* 2:34:01  
* 2:34:68  
* 2:32:59  
* 2:34:66  
* 2:34:42

Promedio:

* 2:34:07

Desviación Estándar:

* 土0:01:34

Debido a que el proceso de la estación es completamente automatizado, la única variación en el tiempo viene de que tan rápido se mueve el operador al dejar el FRED en la estación y llevárselo.

Link al video [https://youtu.be/G-k-KNVUuC8?feature=shared](https://youtu.be/G-k-KNVUuC8?feature=shared)

3. ### *Layout Actualizado de la Celda* {#layout-actualizado-de-la-celda}

El layout final de la estación 2 presenta un diseño minimalista, y a su vez efectivo, para poder delimitar el workspace del robot, se realizó una base a la mesa la cuál delimitará el alcance que el robot podría llegar a tener de esta forma se facilita identificar la zona de trabajo del cobot. El workspace del operador no existe debido a que la estación se encuentra completamente automatizada y por ende no requiere de un espacio designado al operador, finalmente en el layout final podemos ver 12 componentes principales los cuales forman parte del layout, entre estos componentes tenemos el botón de paro de emergencia, el HMI, Monitor, Fixtures, Sensor Infrarrojo, Torreta, etc. Cada uno de estos elementos permiten el funcionamiento adecuado de la estación y buscan efectividad en el proceso.   
![][image40]  
![][image41]  
Figura 39\. Layout de Workspace \- a) Vista superior 3D, b) Vista superior física, c) Leyenda de ubicación.

# **Evaluación y Resultados** {#evaluación-y-resultados}

**Puntaje Total:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Puntos Adicionales**

* **Puntos por Gripper Rediseñado:** 3.5  
* **Presentación de VR de la Celda:** 1  
* **Funcionamiento del FrED:** 5  
* **Interfaz de Monitoreo:** 5

**Total Posible:** 114.5

# **Conclusión** {#conclusión}

El proyecto FrED Factory, es sin duda alguna uno de los proyectos más desafiantes que hay en la carrera, la necesidad de una verdadera integración mecatrónica se ve puesta a prueba durante el desarrollo del FrED Factory en Tec de Monterrey.   
Hablando específicamente de la Estación 2: Electrónica. El reto más grande fue lograr una completa automatización de la estación, esto debido al nivel de precisión de ensamblaje que representaba hacer este proceso de electrónica y la programación de las trayectorias del robot, representaron un reto de alto grado de dificultad.   
Este bloque ha sido uno de los más retadores y completos de nuestra carrera. Disfrutamos cumplir la visión de una estación completamente automatizada con un nuevo diseño de gripper y fixtures alimentadores. Descubrimos los diferentes niveles y reglas de la automatización. Durante el ensamblaje final, aplicamos estos conocimientos para identificar cuellos de botella, tiempos muertos y la falta de posiciones de seguridad. Aprendimos a usar software esencial como Process Simulate y Plant Simulation.  
La carga y variedad de temas en poco tiempo nos obligaron a encontrar soluciones creativas rápidamente. Desarrollamos habilidades en programación de PLC, diseño avanzado en CAD y programación de robots colaborativos, destacando especialmente el pensamiento crítico bajo presión. También vinculamos Process Simulate con lentes de realidad virtual para analizar el proceso y detectar cuellos de botella sin estar físicamente en la estación. 

# **Anexos** {#anexos}

* Archivo principal de programación (Python): [https://github.com/afr2903/FrED-factory/blob/main/team2/main.py](https://github.com/afr2903/FrED-factory/blob/main/team2/main.py)  
* Control remoto para el gripper (Python): [https://github.com/afr2903/FrED-factory/blob/main/team2/gripper\_teleop.py](https://github.com/afr2903/FrED-factory/blob/main/team2/gripper\_teleop.py)  
* Programación del microcontrolador ESP32 (Arduino): [https://github.com/afr2903/FrED-factory/blob/main/team2/gripper/main/main.ino](https://github.com/afr2903/FrED-factory/blob/main/team2/gripper/main/main.ino)  
* Autodesk Viewer Estación: [https://autode.sk/4bAFUF3](https://autode.sk/4bAFUF3)  
* Dibujos técnicos: [https://drive.google.com/file/d/16d6VZvvyFpIjYJ92RVl46owzwP8IH3Dr/view?usp=sharing](https://drive.google.com/file/d/16d6VZvvyFpIjYJ92RVl46owzwP8IH3Dr/view?usp=sharing)  
* Project Management Gantt:[https://github.com/users/afr2903/projects/1/views/4](https://github.com/users/afr2903/projects/1/views/4)

# **Referencias** {#referencias}

\[1\] Ufactory. (s.f). xArm User Manual \[Sitio web\]. Recuperado de [http://download.ufactory.cc/xarm/en/xArm%20User%20Manual.pdf?v=1578910898247](http://download.ufactory.cc/xarm/en/xArm%20User%20Manual.pdf?v=1578910898247)  
\[2\] Mouser electronics (2024). Buck converter.Recuperado de [https://www.mouser.mx/images/marketingid/2018/img/118608864.png?v=070223.0303](https://www.mouser.mx/images/marketingid/2018/img/118608864.png?v=070223.0303)  
\[3\] DigiKey Electronics. (2024). ESP32. Recuperado de [https://www.digikey.com.mx/en/products/detail/espressif-systems/ESP32-C3-DEVKITM-1/13684315](https://www.digikey.com.mx/en/products/detail/espressif-systems/ESP32-C3-DEVKITM-1/13684315)  
\[4\] M. SALDAÑA. (s. f.). Normativa de Robots Colaborativos (Cobots) y su influencia en la. Prevención Integral & ORP Conference. [https://www.prevencionintegral.com/canal-orp/papers/orp-2019/normativa-robots-colaborativos-cobots-su-influencia-en-prevencion-riesgos-laborales](https://www.prevencionintegral.com/canal-orp/papers/orp-2019/normativa-robots-colaborativos-cobots-su-influencia-en-prevencion-riesgos-laborales) 
