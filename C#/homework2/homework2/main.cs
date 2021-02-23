using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Reflection;
namespace homework1
{
    class Program
    {
        static void Menu()
        {
            Console.Write("\nA to add" +
                        "\nD to delete" +
                        "\nE to edit" +
                        "\nS to sort" +
                        "\nF to search" +
                        "\nP to show all" +
                        "\nQ to quit\n");
        }

        static dynamic EnterValues(PropertyInfo property)
        {
            string new_data;
            Console.WriteLine($"Enter new value for {property.Name}:");

            if (property.PropertyType.Equals(typeof(DateTime)))
            {
                string data = "";
                Console.WriteLine("Enter date:");
                data += Console.ReadLine() + "T";
                Console.WriteLine("Enter time:");
                data += Console.ReadLine();
                new_data = data;
            }
            else
                new_data = Console.ReadLine();
            try
            {
                var toReturn = Convert.ChangeType(new_data, property.PropertyType, System.Globalization.CultureInfo.InvariantCulture);
                return toReturn;
            }
            catch 
            {
                throw new Exception($"Wrong type of {property.Name}");
            }
        }
        static void Main()
        {
            bool flag = true;
            char givOption;
            string fileName;
            do
            {
                Console.WriteLine("Enter file name:");
                fileName = Console.ReadLine();
            }
            while (!Validation.ValidateFileName(fileName));

            Type to_work = typeof(Event);
            
            Collection<Event> allObjects = new Collection<Event>(fileName);
            
            PropertyInfo[] object_properties = to_work.GetProperties();
            while (flag)
            {
                Menu();
                givOption = Convert.ToChar(Console.ReadLine());
                switch (givOption)
                {
                    case 'Q': flag = false; break;
                    case 'A':
                            
                        object toAdd = Activator.CreateInstance(to_work);
                        try
                        {
                            foreach (PropertyInfo x in object_properties)
                                to_work.GetProperty(x.Name).SetValue(toAdd, EnterValues(x));
                            if (allObjects.IsPresent((int)to_work.GetProperty("ID", BindingFlags.IgnoreCase | BindingFlags.Public | BindingFlags.Instance).GetValue(toAdd)))
                            {
                                Console.WriteLine("Object with such ID already exists");
                            }
                            else
                            {
                                allObjects.Add(toAdd);
                                Console.WriteLine("Object successfully added to collection");
                                allObjects.Overwrite();
                            }
                        }
                        catch (Exception e)
                        {
                            Console.WriteLine(e.Message);
                            if (e.InnerException != null)
                                Console.WriteLine(e.InnerException.Message);
                        }
                        break;

                    case 'D':
                        Console.Write(allObjects.PrintAll());
                        Console.WriteLine("Select the object to delete:");
                        string to_delete = Console.ReadLine();
                        Console.WriteLine(allObjects.DeleteOne(to_delete));
                        allObjects.Overwrite(); break;

                    case 'E':
                        Console.Write(allObjects.PrintAll());
                        Console.WriteLine("Select the object to edit:");
                        string to_edit = Console.ReadLine();
                        object objectToEdit = allObjects.FindByID(to_edit);
                        if (objectToEdit != null)
                        {
                            Console.Write(objectToEdit);
                            Console.WriteLine("Select the property to edit:");
                            string choice = Console.ReadLine();
                            PropertyInfo chosenProperty = object_properties.SingleOrDefault(r => r.Name.Equals(choice));
                            if (chosenProperty != null)
                            {
                                try
                                {
                                    var new_data = EnterValues(chosenProperty);
                                    to_work.GetProperty(choice).SetValue(objectToEdit, new_data);
                                    Console.Write($"Success\n{objectToEdit}");
                                    allObjects.Overwrite();
                                }
                                catch (Exception e)
                                {
                                    if (e.InnerException != null)
                                        Console.WriteLine(e.InnerException.Message);
                                    else
                                        Console.WriteLine(e.Message);
                                }
                            }
                            else
                                Console.WriteLine("No such property");
                        }
                        else
                            Console.WriteLine("No such item");
                        break;

                    case 'S':
                        Console.WriteLine("Select the property to sort by:");
                        string parameter = Console.ReadLine();
                        if (object_properties.SingleOrDefault(r => r.Name.Equals(parameter)) != null)
                        {
                            if (allObjects.Sorting(parameter))
                            {
                                Console.WriteLine("Success");
                                Console.Write(allObjects.PrintAll());
                            }
                            else
                                Console.WriteLine("Nothing to sort");
                        }
                        else
                            Console.WriteLine("No such property");
                        break;

                    case 'F':
                        Console.WriteLine("Enter what to find:");
                        string to_find = Console.ReadLine();
                        Console.Write(allObjects.FindObjects(to_find));
                        break;

                    case 'P': Console.Write(allObjects.PrintAll()); break;

                    default: Console.WriteLine("No such option"); break;
                } 
            }
            Console.WriteLine("The end");
            Console.ReadKey();
        }
    }
}
