class WebSocketClient {
    private socket!: WebSocket;
    private isConnected: boolean = false;
  
    constructor(private url: string) {}
  
    connect(): Promise<void> {
      return new Promise((resolve, reject) => {
        this.socket = new WebSocket(this.url);
  
        this.socket.onopen = () => {
          console.log("WebSocket connection opened");
          this.isConnected = true;
          resolve();
        };
  
        this.socket.onerror = (error) => {
          console.error("WebSocket connection error", error);
          reject(error);
        };
  
        this.socket.onclose = () => {
          console.log("WebSocket connection closed");
          this.isConnected = false;
        };
      });
    }
  
    sendMessage(message: string): Promise<number | null> {
      return new Promise((resolve, reject) => {
        if (!this.isConnected) {
          reject("WebSocket is not connected");
          return;
        }
  
        this.socket.send(message);
  
        this.socket.onmessage = (event) => {
          console.log("Message received from server:", event.data);
  
          // Parse the response
          const parsedData = parseFloat(event.data);
  
          if (!isNaN(parsedData)) {
            resolve(parsedData);
          } else {
            resolve(null); // Handle null if no valid data is received
          }
        };
  
        this.socket.onerror = (error) => {
          console.error("Error receiving message", error);
          reject(error);
        };
      });
    }
  
    disconnect(): void {
      if (this.socket) {
        this.socket.close();
      }
    }
  }
  
  // Usage Example
  const websocketUrl = "ws://localhost:8080/websocket"; // Adjust your server URL if needed
  const websocketClient = new WebSocketClient(websocketUrl);
  
  (async () => {
    try {
      await websocketClient.connect();
      console.log("Connected to WebSocket");
  
      // Send a currency name to fetch current data
      const currencyName = "BTC"; // Replace with the desired currency name
      const price = await websocketClient.sendMessage(currencyName);
  
      if (price !== null) {
        console.log(`The price of ${currencyName} is: ${price}`);
      } else {
        console.error(`Currency data not found for: ${currencyName}`);
      }
  
      // Disconnect the WebSocket
      websocketClient.disconnect();
    } catch (error) {
      console.error("Error:", error);
    }
  })();
  