using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Ztore
{
    public partial class Welcome : Form
    {
        public Welcome()
        {
            InitializeComponent();
        }


        private void signUpButton_Click(object sender, EventArgs e)
        {
            // Redirect to the sign-up form
            SignUpForm signUpForm = new SignUpForm();
            signUpForm.ShowDialog();
        }

        private async void signInButton_Click(object sender, EventArgs e)
        {
            // Redirect to the sign-up form
            string username = usernameTextBox.Text;
            string password = passwordTextBox.Text;
            Shopping shopping = new Shopping();
            bool userValid = await Customer.validateSignInAsync(username, password);
            if (userValid)
            {
                MessageBox.Show("User is ok");
                this.Hide();
                shopping.ShowDialog();
            }

            
            

        }

        private void Welcome_Load(object sender, EventArgs e)
        {

        }
    }
}
