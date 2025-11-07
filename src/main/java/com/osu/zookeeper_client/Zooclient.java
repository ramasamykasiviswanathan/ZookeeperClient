package com.osu.zookeeper_client;

import java.io.IOException;
import java.io.UnsupportedEncodingException;

import org.apache.zookeeper.CreateMode;
import org.apache.zookeeper.KeeperException;
import org.apache.zookeeper.ZooDefs;
import org.apache.zookeeper.ZooKeeper;
import org.springframework.cloud.zookeeper.discovery.configclient.ZookeeperDiscoveryClientConfigServiceBootstrapConfiguration;

public class Zooclient {
    private static ZooKeeper zkeeper;
    private final ZKConnection zkConnection;

    public Zooclient() {
    	zkConnection = new ZKConnection();
    	try {
			zkeeper = zkConnection.connect("localhost");
		} catch (IOException | InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
    }

    public void closeConnection() {
        try {
			zkConnection.close();
		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
    }

    public void create(String path, byte[] data) throws KeeperException, InterruptedException {
 
        zkeeper.create(
          path, 
          data, 
          ZooDefs.Ids.OPEN_ACL_UNSAFE, 
          CreateMode.PERSISTENT);
    }

    public Object getZNodeData(String path, boolean watchFlag) throws KeeperException, InterruptedException {
 
        byte[] b = null;
        b = zkeeper.getData(path, null, null);
        try {
			return new String(b, "UTF-8");
		} catch (UnsupportedEncodingException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
        return null;
    }

    public void update(String path, byte[] data) throws KeeperException, 
      InterruptedException {
        int version = zkeeper.exists(path, true).getVersion();
        zkeeper.setData(path, data, version);
    }
}