using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace homework1
{
    static class Validation
    {
        public static int ValidateId(int given_input)
        {
            if (given_input <= 0)
            {
                throw new Exception("Id has to be larger than 0");
            }
            return given_input;
        }

        public static double ValidatePrice(double given_input)
        {
            if (given_input < 0)
            {
                throw new Exception("Price is lower than 0");
            }
            return Math.Round(given_input, 2);
        }
        public static double ValidateDuration(double given_input)
        {
            if (given_input <= 0)
            {
                throw new Exception("Duration has to be positive");
            }
            return Math.Round(given_input, 1);
        }
        public static DateTime ValidateDateTime(string given_input)
        {
            try
            {
                DateTime toReturn = DateTime.ParseExact(given_input, "yyyy MM dd HH mm ss", System.Globalization.CultureInfo.InvariantCulture);
                return toReturn;
            }
            catch
            {
                throw new Exception("Input is not Date & Time");
            }
        }
        public static RestaurantNames ValidateRestName(dynamic given_input)
        {
            try
            {
                int new_value = Convert.ChangeType(given_input, typeof(int));
                if (!typeof(RestaurantNames).IsEnumDefined(new_value))
                {
                    throw new Exception("No such restaurant");
                }
                return (RestaurantNames)new_value;
            }
            catch (Exception e) when (e.Message != "No such restaurant")
            {
                throw new Exception("Restaurant selection is done using a number from list");
            }
        }
        public static bool ValidateFileName(string given_input)
        {
            try
            {
                StreamReader file = File.OpenText(given_input);
                file.Close();
                return true;
            }
            catch
            {
                return false;
            }
        }
    }
}
