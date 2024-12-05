const mysql = require("mysql");
const dotenv = require("dotenv");
dotenv.config();

console.log("env file port: ", process.env.MYSQL_PORT);

const pool = mysql.createPool({
    connectionLimit: 10,
    host: process.env.MYSQL_HOST,
    user: process.env.MYSQL_USER,
    password: process.env.MYSQL_ROOT_PASSWORD,
    database: process.env.MYSQL_DATABASE,
    port: process.env.MYSQL_PORT
});
exports.pool = pool;