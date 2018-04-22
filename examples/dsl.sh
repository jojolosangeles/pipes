set -x
python3 ../pipes/pipe.py processor dsl2object.dsl_engine.DSL_Engine input stream file ../data/ddia.figure5-2 output stream file dsljson/ddia.figure5-2.json
python3 ../pipes/pipe.py processor dsl2object.dsl_engine.DSL_Engine input stream file ../data/ddia.figure5-3 output stream file dsljson/ddia.figure5-3.json
python3 ../pipes/pipe.py processor dsl2object.dsl_engine.DSL_Engine input stream file ../data/ddia.figure5-4 output stream file dsljson/ddia.figure5-4.json
python3 ../pipes/pipe.py processor dsl2object.dsl_engine.DSL_Engine input stream file ../data/ddia.figure5-5 output stream file dsljson/ddia.figure5-5.json
python3 ../pipes/pipe.py processor dsl2object.dsl_engine.DSL_Engine input stream file ../data/ddia.figure8-3 output stream file dsljson/ddia.figure8-3.json
python3 ../pipes/pipe.py processor dsl2object.dsl_engine.DSL_Engine input stream file ../data/ddia.figure8-4 output stream file dsljson/ddia.figure8-4.json
