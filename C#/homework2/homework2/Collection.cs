using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

namespace homework1
{
    class Collection<T>
    {
        private List<T> coll = new List<T>();
        private string filePath;
        public Collection(string fileName)
        {
            JArray obj;
            filePath = fileName;
            using (StreamReader file = File.OpenText(filePath))
            using (JsonTextReader reader = new JsonTextReader(file))
            {
                obj = (JArray)JToken.ReadFrom(reader);
            }
            Dictionary<string, string>[] objects = obj.ToObject<Dictionary<string, string>[]>();
            int obj_counter = 1;
            foreach (Dictionary<string, string> x in objects)
            {
                Console.WriteLine($"\nObject {obj_counter}:");
                bool correct_obj = true;
                T new_object = (T)typeof(T).GetConstructor(new Type[0]).Invoke(null);
                foreach (KeyValuePair<string, string> y in x)
                {
                    try
                    {
                        typeof(T).GetProperty(y.Key).SetValue(new_object, y.Value);
                    }
                    catch (Exception e)
                    {
                        Console.WriteLine(e.InnerException.Message);
                        correct_obj = false;
                    }
                }
                if (correct_obj)
                {
                    Console.WriteLine($"Object {obj_counter} initialized successfully");
                    this.Add(new_object);
                }
                else
                {
                    Console.WriteLine($"Object {obj_counter} failed to initialize");
                }
                obj_counter++;
            }
        }

        public void Add(T to_add)
        {
            coll.Add(to_add);
        }

        public bool IsPresent(int giv_id)
        {
            foreach (T x in coll)
            {
                if (typeof(T).GetProperty("id", BindingFlags.IgnoreCase | BindingFlags.Public | BindingFlags.Instance).GetValue(x) == (object)giv_id)
                    return true;
            }
            return false;
        }
        public string PrintAll()
        {
            string to_return = "\n";
            foreach (T x in coll)
            {
                to_return += x.ToString() + "\n";
            }
            return to_return;
        }
        
        public string DeleteOne(string input)
        {
           T itemToRemove = this.FindByID(input);
            if (itemToRemove != null)
            {
                this.coll.Remove(itemToRemove);
                return "Successfully removed";
            }
            return "Failed to remove, no such id";
        }

        public string FindObjects(string input)
        {
            string found = "\n";
            bool added;
            foreach (T x in coll)
            {
                added = false;
                foreach (System.Reflection.PropertyInfo y in typeof(T).GetProperties())
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
        public T FindByID(string to_find)
        {
            T itemToReturn = this.coll.SingleOrDefault(r => Convert.ToString(typeof(T).GetProperty("id", BindingFlags.IgnoreCase | BindingFlags.Public | BindingFlags.Instance).GetValue(r)).Equals(to_find));
            return itemToReturn;
        }

        public bool Sorting(string sort_parameter)
        {
            if (coll.Any())
            {
                List<T> sorted;
                if (typeof(T).GetProperty(sort_parameter).GetValue(coll[0]).GetType().Equals(typeof(string)))
                    sorted = coll.OrderBy(r => Convert.ToString(typeof(T).GetProperty(sort_parameter).GetValue(r)).ToLower()).ToList();
                else
                    sorted = coll.OrderBy(r => typeof(T).GetProperty(sort_parameter).GetValue(r)).ToList();
                coll = sorted;
                return true;
            }
            else
                return false;
        }

        public void Overwrite()
        {
            List<T> sorted = coll.OrderBy(r => typeof(T).GetProperty("id", BindingFlags.IgnoreCase | BindingFlags.Public | BindingFlags.Instance).GetValue(r)).ToList();
            JArray array = new JArray { };
            foreach (T x in sorted)
            {
                JObject singleObject = JObject.Parse(JsonConvert.SerializeObject(x, new JsonSerializerSettings {DateFormatString = "yyyy MM dd HH mm ss" }));
                array.Add(singleObject);
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
