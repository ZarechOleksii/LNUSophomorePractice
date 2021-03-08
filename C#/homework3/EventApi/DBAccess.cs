using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Npgsql;
using System.Data;

namespace EventApi
{
    public class DBAccess
    {
        static readonly string ConnectionString = "Host=localhost;Username=postgres;Password=12345;Database=Practice";
        static NpgsqlConnection con;

        public static void OpenConection()
        {
            con = new NpgsqlConnection(ConnectionString);
            con.Open();
        }
        public static void CloseConnection()
        {
            con.Close();
        }
        public static void ExecuteQueries(string Query_)
        {
            NpgsqlCommand cmd = new(Query_, con);
            cmd.ExecuteNonQuery();
        }
        public static NpgsqlDataReader DataReader(string Query_)
        {
            NpgsqlCommand cmd = new(Query_, con);
            NpgsqlDataReader dr = cmd.ExecuteReader();
            return dr;
        }
    }
}
