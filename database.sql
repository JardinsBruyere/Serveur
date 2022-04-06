CREATE TABLE Sensor (
  Id INTEGER PRIMARY KEY AUTOINCREMENT,
  Type INTEGER,
  DateAdded DATETIME DEFAULT (datetime('now','localtime')),
  Station INTEGER,
  Name varchar(100), MacAdress varchar(100),
  FOREIGN KEY (Type) REFERENCES SensorTypes(Id),
  FOREIGN KEY (Station) REFERENCES Station(Id)
);
CREATE TABLE SensorTypes (
  Id INTEGER PRIMARY KEY AUTOINCREMENT,
  Unit varchar(100)
);
CREATE TABLE Station (
  Id INTEGER PRIMARY KEY AUTOINCREMENT,
  Name varchar(100)
);
CREATE TABLE SensorReading (
  Id INTEGER PRIMARY KEY AUTOINCREMENT,
  SensorId INTEGER,
  DateAdded DATETIME DEFAULT (datetime('now','localtime')),
  Value INTEGER,
  FOREIGN KEY (SensorId) REFERENCES Sensor(Id)
);
CREATE TABLE macARP(
  Id integer primary key autoincrement,
  mac varchar(100)
);