## **Servidor RabbitMQ**

 - Aqui se encontram scripts para serem executados no servidor **RabbitMQ**;
   
 - O protocolo definido foi o **AMQP**, utilizando o modelo de **tópicos**;
 
 - As bibliotecas python estão descritas no arquivo
   '**rabbit_requirements.txt**', a serem instalados com o '**pip**' pelo comando:

    - sudo pip install -r rabbit_requirements.txt
 
 - Para utilizar o MQTT com o Spark, habilitar o plugin MQTT do RabbitMQ com o seguinte comando:

    - sudo rabbitmq-plugins enable rabbitmq_mqtt

 - O arquivo **rabbitmq.config** deve ser colocar no diretório **/etc/rabbitmq/**, para que funcione a comunicação MQTT;
