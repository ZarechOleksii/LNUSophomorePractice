using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

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
        static void Rests()
        {
            int[] values = (int[]) Enum.GetValues(typeof(RestaurantNames));

            Console.WriteLine($"Available Restaurants (choose a number):");
            foreach (int value in values)
            {
                Console.WriteLine($"{value} - {Enum.GetName(typeof(RestaurantNames), value)}");
            }
        }
        static string EnterValues(string parameter)
        {
            string new_data;
            string[] datesTimes = { "year", "month", "day", "hour", "minute" };
            Console.WriteLine($"Enter new value for {parameter}:");

            if (parameter == "RestName")
                Rests();

            if (parameter == "DateTime")
            {
                string data = "";
                foreach (string y in datesTimes)
                {
                    Console.WriteLine($"Enter {y}:");
                    data += Console.ReadLine() + " ";
                }
                data += "00";
                new_data = data;
            }
            else
                new_data = Console.ReadLine();
            return new_data;
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
            Collection<Event> allEvents = new Collection<Event>(fileName);
            string[] event_properties = new string[6]
            {
                "Id", "Title", "Duration", "Price", "DateTime", "RestName"
            };
            while (flag)
            {
                try
                {
                    Menu();
                    givOption = Convert.ToChar(Console.ReadLine());
                    switch (givOption)
                    {
                        case 'Q': flag = false; break;
                        case 'A':
                            Dictionary<string, string> dictToCreate = new Dictionary<string, string> { };
                            
                            foreach (string x in event_properties)
                            {
                                string new_data = EnterValues(x);
                                dictToCreate.Add(x, new_data);
                            }

                            Event toAdd = new Event(dictToCreate);
                            if (toAdd.Correct())
                                if (allEvents.IsPresent(toAdd.Id))
                                {
                                    Console.WriteLine("Event with such ID already exists");
                                }
                                else 
                                {
                                    allEvents.Add(toAdd);
                                    Console.WriteLine("Event successfully added to collection");
                                    allEvents.Overwrite();
                                }
                            else
                            {
                                Console.WriteLine("There were mistakes in your input:");
                                toAdd.PrintErrors();
                            }
                            break;
                        case 'D':
                            Console.Write(allEvents.PrintAll());
                            Console.WriteLine("Select the Event to delete:");
                            string to_delete = Console.ReadLine();
                            Console.WriteLine(allEvents.DeleteOne(to_delete));
                            allEvents.Overwrite(); break;
                        case 'E':
                            Console.Write(allEvents.PrintAll());
                            Console.WriteLine("Select the Event to edit:");
                            string to_edit = Console.ReadLine();
                            Event eventToEdit = allEvents.FindByID(to_edit);
                            if (eventToEdit != null)
                            {
                                Console.Write(eventToEdit);
                                Console.WriteLine("Select the property to edit:");
                                string choice = Console.ReadLine();
                                if (event_properties.SingleOrDefault(r => r.Equals(choice)) != null)
                                {
                                    string new_data = EnterValues(choice);
                                    try
                                    {
                                        typeof(Event).GetProperty(choice).SetValue(eventToEdit, new_data);
                                        Console.Write($"Success\n{eventToEdit}");
                                        allEvents.Overwrite();
                                    }
                                    catch (Exception e)
                                    {
                                        Console.WriteLine(e.InnerException.Message);
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
                            if (event_properties.SingleOrDefault(r => r.Equals(parameter)) != null)
                            {
                                if (allEvents.Sorting(parameter))
                                {
                                    Console.WriteLine("Success");
                                    Console.Write(allEvents.PrintAll());
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
                            Console.Write(allEvents.FindObjects(to_find));
                            break;
                        case 'P': Console.Write(allEvents.PrintAll()); break;
                        default: Console.WriteLine("No such option"); break;
                    }
                    
                }
                catch (Exception e)
                {
                    Console.WriteLine(e.ToString());
                    Console.WriteLine("Mistakes were made");
                    Console.ReadKey();
                }
            }
            Console.WriteLine("The end");
            Console.ReadKey();
        }
    }
}
