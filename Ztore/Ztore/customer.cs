using Communicator;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using Ztore.exceptions;

namespace Ztore
{
    public  class Customer
    {
        public string userId;
        public string password;
        public string firstName;
        public string lastName;
        public string email;
        public string address;
        public string phoneNumber;
        public Customer(string userId, string password, string firstName, string lastName, string email, string address, string phoneNumber)
        {
            this.userId = userId;
            this.password = password;
            this.firstName = firstName;
            this.lastName = lastName;
            this.email = email;
            this.address = address;
            this.phoneNumber = phoneNumber;
        }


        public static async Task<bool> validateSignInAsync(string userId, string password)
        {
            if (userId == "" || password == "")
            {
                MessageBox.Show("Please fill bith userId and password");
                return false;
            }
            CommunicatorHanddler communicator = CommunicatorHanddler.Instance;
            string my_json = $"{{'customer_id': '{userId}', 'customer_password': '{password}'}}";
            try
            {
                string response = (await communicator.PostDataToServerAsync("getUser", my_json));
                return true;
            }

            catch (Exception ex)
            {
                MessageBox.Show(ex.Message);
                return false;
            }

        }
    }
}
