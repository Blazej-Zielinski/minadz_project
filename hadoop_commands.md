# Hadoop comands cheat sheet

Hadoop web console url
```
    http://localhost:9870
```

leave Hadoop safe mode
```
    hadoop dfsadmin -safemode leave
```

start namenodes
```
    /sbin/start-dfs.sh
```

make directory with name `dirname`
```
    hdfs dfs -mkdir /dirname
```

copy file from local FS to HDFS `dirname` directory
```
    hdfs dfs -copyFromLocal 
    /home/user/folder/file.csv 
    /dirname
```

run job using streaming hadoop api
```
    hadoop jar /home/kuba/minadzd/minadz_project/jars/hadoop-streaming-2.7.3.jar 
    -input /user/kuba/project/input/alcohol-consumption-vs-gdp-per-capita.csv 
    -output /user/kuba/project/output 
    -mapper /home/kuba/minadzd/minadz_project/damaged_data_mapper.py 
    -reducer /home/kuba/minadzd/minadz_project/damaged_data_reducer.py
```

read output file from HDFS
```
    hdfs dfs -cat /user/kuba/project/output/*
```

remove directory with all its content
```
    hdfs dfs -rm -r /user/kuba/project/output
```