using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

namespace homework1
{
    class Collection
    {
        private List<Event> coll = new List<Event>();
        private string filePath;
        public Collection(string fileName)
        {
            JArray obj;
            filePath = "D:\\School\\C# LNY\\Navch Prakt\\homework1\\homework1\\" + fileName;
            using (StreamReader file = File.OpenText(filePath))
            using (JsonTextReader reader = new JsonTextReader(file))
            {
                obj = (JArray)JToken.ReadFrom(reader);
            }
            Dictionary<string, string>[] events = obj.ToObject<Dictionary<string, string>[]>();
            int obj_counter = 1;
            foreach (Dictionary<string, string> x in events)
            {
                Event new_event = new Event(x);
                if (new_event.Correct())
                {
                    Console.WriteLine($"Object {obj_counter} initialized successfully");
                    this.Add(new_event);
                }
                else
                {
                    Console.WriteLine($"Object {obj_counter} failed to initialize,");
                    new_event.PrintErrors();
                }
                obj_counter++;
            }
        }

        public void Add(Event to_add)
        {
            coll.Add(to_add);
        }

        public bool Present(int giv_id)
        {
            foreach (Event x in coll)
            {
                if (x.Id == giv_id)
                    return true;
            }
            return false;
        }
        public string PrintAll()
        {
            string to_return = "\n";
            foreach (Event x in coll)
            {
                to_return += x.ToString() + "\n";
            }
            return to_return;
        }
        
        public string DeleteOne(string input)
        {
            Event itemToRemove = this.FindByID(input);
            if (itemToRemove != null)
            {
                this.coll.Remove(itemToRemove);
                return "Successfully removed";
            }
            return "Failed to remove, no such id";
        }

        public string FindEvents(string input)
        {
            string found = "\n";
            bool added;
            foreach (Event x in coll)
            {
                added = false;
                foreach (System.Reflection.PropertyInfo y in typeof(Event).GetProperties())
                {
                    if (added)
                        break;
                    int symbols = input.Length;
                    int iteration = 0;
                    string propertyValue = Convert.ToString(y.GetValue(x));
                    while (iteration + symbols <= propertyValue.Length)
                    {
                        if (propertyValue.Substring(iteration, symbols).Equals(input))
                        {
                            found += x.ToString() + "\n";
                            added = true;
                            break;
                        }
                        else
                            iteration++;
                    }
                }
            }
            return found;
        }
        public Event FindByID(string to_find)
        {
            Event itemToReturn = this.coll.SingleOrDefault(r => Convert.ToString(r.Id).Equals(to_find));
            return itemToReturn;
        }
        
        public void Sorting(string sort_parameter)
        {
            
            List<Event> sorted;
            if (sort_parameter.Equals("Title") || sort_parameter.Equals("RestName"))
                sorted = coll.OrderBy(r => Convert.ToString(typeof(Event).GetProperty(sort_parameter).GetValue(r)).ToLower()).ToList();
            else
                sorted = coll.OrderBy(r => typeof(Event).GetProperty(sort_parameter).GetValue(r)).ToList();
            coll = sorted;
        }

        public void Overwrite()
        {
            List<Event> sorted = coll.OrderBy(r => r.Id).ToList();
            JArray array = new JArray { };
            foreach (Event x in sorted)
            {
                JObject singleEvent = JObject.Parse(JsonConvert.SerializeObject(x, new JsonSerializerSettings {DateFormatString = "yyyy MM dd HH mm ss" }));
                array.Add(singleEvent);
            }
            using (StreamWriter file = File.CreateText(filePath))
            using (JsonTextWriter writer = new JsonTextWriter(file))
            {
                writer.Formatting = Formatting.Indented;
                array.WriteTo(writer);
            }
        }
    }
}
