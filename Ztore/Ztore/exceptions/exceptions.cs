using System;

namespace Ztore.exceptions
{

    class BadStatusCode : Exception
    {
        public BadStatusCode(string message) : base(message)
        { }


    }

    class InvalidData : Exception
    {
        public InvalidData(string message) : base(message)
        { }


    }
}
