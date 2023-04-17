package com.example.pulsarworkshop;

import java.io.File;
import java.util.Map;

import org.apache.commons.lang3.StringUtils;

import com.example.pulsarworkshop.exception.InvalidParamException;
import com.example.pulsarworkshop.util.ClientConnConf;
import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;

abstract public class S4RCmdApp extends PulsarWorkshopCmdApp {
    protected final static String API_TYPE = "rabbitmq-s4r";
    int S4RPort = 5672;
    String S4RQueueName = "s4r-default-queue";
    String S4RRabbitMQHost = "localhost";
    String S4RPassword = "";
    String S4RUser = "";
    String S4RVirtualHost = "";
    String S4RMessage = "";
    ConnectionFactory S4RFactory;
    Connection connection;
    Channel channel;
    int MsgReceived = 0;
    File rabbitmqConnfFile;
    Boolean AstraInUse;    
    public S4RCmdApp(String appName, String[] inputParams) {
        super(appName, inputParams);
        // Add the S4R/RabbitMQ specific CLI options that are common to all S4R/RabbitMQ client applications
        addOptionalCommandLineOption("q", "s4rqueue", true, "S4R Pulsar RabbitMQ queue name.");
        addOptionalCommandLineOption("a", "useAstra", true, "Use Astra Streaming for RabbitMQ server.");
        addOptionalCommandLineOption("m", "s4rmessage", true, "S4R Pulsar RabbitMQ message to send, otherwise a default is used.");

    }
    @Override
    public void processExtendedInputParams() throws InvalidParamException {        
        String queueName = processStringInputParam("s4rqueue");
        if (!StringUtils.isBlank(queueName)) {
            S4RQueueName = queueName;
        }
        rabbitmqConnfFile = processFileInputParam("connFile");
        if(rabbitmqConnfFile == null) {
            throw new InvalidParamException("rabbitmq.conf file must be provided.");
        }
        processRabbitMQConfFile();
        String useAstra= processStringInputParam("useAstra");
        if(useAstra != null) {
            AstraInUse = true;
        } else {
            AstraInUse = false;
        }
        String msgToSend = processStringInputParam("s4rmessage");
        if (!StringUtils.isBlank(msgToSend)) {
            S4RMessage = msgToSend;
        }
    }    
    private void processRabbitMQConfFile() {
        ClientConnConf connCfgConf = null;
        connCfgConf = new ClientConnConf(rabbitmqConnfFile);
        connCfgConf.getClientConfMap();
        Map<String, String> clientConnMap = connCfgConf.getClientConfMap();

        String port = clientConnMap.get("port");
        S4RPort = Integer.parseInt(port);  
        
        S4RRabbitMQHost = clientConnMap.get("host");
        S4RPassword = clientConnMap.get("password");
        S4RUser = clientConnMap.get("username");
        if(S4RUser == null) {
            S4RUser = ""; // null will cause connection errors, set to blank ""
        }
        S4RVirtualHost = clientConnMap.get("virtual_host");
    }    
}
