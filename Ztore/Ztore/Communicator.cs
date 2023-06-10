using System.Net;
using System.Text;
using System.Net.Http;
using System.Threading.Tasks;
using System;
using Ztore;
using Ztore.exceptions;

namespace Communicator
{
    public sealed class CommunicatorHanddler
    {
        private static CommunicatorHanddler instance = null;
        private static readonly object padlock = new object();
        private string FlaskServerIp;
        private int FlaskServerPort;
        private HttpClient client;

        private CommunicatorHanddler()
        {
            this.FlaskServerIp = Constnas.FlaskServerIp;
            this.FlaskServerPort = Constnas.FlaskServerPort;
            this.client = new HttpClient();
        }

        public static CommunicatorHanddler Instance
        {
            get
            {
                lock (padlock)
                {
                    if (instance == null)
                    {
                        instance = new CommunicatorHanddler();
                    }
                    return instance;
                }
            }
        }

        public async Task<string> PostDataToServerAsync(string page_name, string myJson)
        // Sends post requests to the flask server
        {
            string fullPagePath = $"{this.FlaskServerIp}:{this.FlaskServerPort}/{page_name}";
            Console.WriteLine($"Posting to {fullPagePath}");
            HttpResponseMessage response = await this.client.PostAsync(fullPagePath, new StringContent(myJson, Encoding.UTF8, "application/json"));
            if (response.IsSuccessStatusCode)
            {
                Console.WriteLine($"Responde: {response.IsSuccessStatusCode}");
                string data = await response.Content.ReadAsStringAsync();
                if (data.StartsWith("ERROR:"))
                {
                    throw new InvalidData(data);
                }
     

            }
            throw new BadStatusCode($"Error, recieved {(int)response.StatusCode} from the server");

        }

        public static string ClearResponse(string response)
        {
            int index = response.IndexOf("OK: ", StringComparison.OrdinalIgnoreCase);
            response.Remove(index, "OK: ".Length);
        }

        public void PrintMessage(string message)
        {
            Console.WriteLine(message);
        }
    }
}