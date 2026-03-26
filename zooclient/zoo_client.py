from kazoo.client import KazooClient
from kazoo.exceptions import NoNodeError
import multiprocessing
import concurrent.futures

'172.17.24.2:2181,172.17.24.3:2181,172.17.24.4:2181,172.17.24.5:2181,172.17.24.1:2181'


def get_children(index = 0):
    zk = KazooClient(hosts='172.17.24.2:2181,172.17.24.3:2181,172.17.24.4:2181,172.17.24.5:2181,172.17.24.1:2181')
    zk.start()

    path = "/"
    session_id = None
    try:
        if zk.connected:
            session_id, password = zk.client_id
            print(f"Connected to ZooKeeper with session ID: {session_id}")
        if zk.exists(path):
            children = zk.get_children(path)
            print(f"Children of {path}: {children}")
            
            # Optional: Get data for each child
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
        results = executor.map(get_children, range(5))
        for result in results:
            print(result)