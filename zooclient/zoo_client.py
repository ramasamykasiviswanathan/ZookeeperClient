from kazoo.client import KazooClient
from kazoo.exceptions import NoNodeError
import multiprocessing
import concurrent.futures

# server.2=172.17.65.2:2888:3888
# server.3=172.17.65.3:2888:3888 #Leader
# server.4=172.17.65.4:2888:3888
# server.5=172.17.65.5:2888:3888
# server.1=172.17.65.1:2888:3888


def get_children(index = 0):
    # zk = KazooClient(hosts='172.17.65.2:2181,172.17.65.3:2181,172.17.65.4:2181,172.17.65.5:2181,172.17.65.1:2181')
    # zk = KazooClient(hosts='172.17.65.3:2181') #Leader
    # zk = KazooClient(hosts='172.17.65.2:2181') #Follower
    # zk = KazooClient(hosts='172.17.65.4:2181') #Follower
    print(f"Connecting to ZooKeeper server at 172.17.65.{index}:2181")
    zk = KazooClient(hosts=f'172.17.65.{index}:2181')
    zk.start()

    path = "/"
    session_id = None
    try:
        if zk.connected:
            session_id, password = zk.client_id
            print(f"Connected to ZooKeeper with session ID: {session_id}")
            
            # print(zk.create("/follower", f"{session_id}".encode('utf-8'), makepath=True))

        if zk.exists(path):
            children = zk.get_children(path)
            print(f"Children of {path}: {children}")
            
            for child in children:
                child_path = f"{path}/{child}"
                data, stat = zk.get(child_path)
                print(f"Child: {child}, Data: {data.decode('utf-8')}")
        else:
            print(f"Node {path} does not exist.")
            return session_id

    except NoNodeError:
        print("Node not found")

    else: 
        return session_id
        
    finally:
        zk.stop()
        zk.close()

if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        results = executor.map(get_children, range(1,6))
        for result in results:
            print(result)