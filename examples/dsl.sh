set -x
rm -rf dsljson
rm -rf dslgist
mkdir dsljson
mkdir dslgist
python3 ../pipes/pipe.py processor dsl2object.dsl_engine.DSL_Engine input stream file ../data/ddia.figure5-2 output stream file dsljson/ddia.figure5-2.json
python3 ../pipes/pipe.py processor dsl2object.dsl_engine.DSL_Engine input stream file ../data/ddia.figure5-3 output stream file dsljson/ddia.figure5-3.json
python3 ../pipes/pipe.py processor dsl2object.dsl_engine.DSL_Engine input stream file ../data/ddia.figure5-4 output stream file dsljson/ddia.figure5-4.json
python3 ../pipes/pipe.py processor dsl2object.dsl_engine.DSL_Engine input stream file ../data/ddia.figure5-5 output stream file dsljson/ddia.figure5-5.json
python3 ../pipes/pipe.py processor dsl2object.dsl_engine.DSL_Engine input stream file ../data/ddia.figure8-3 output stream file dsljson/ddia.figure8-3.json
python3 ../pipes/pipe.py processor dsl2object.dsl_engine.DSL_Engine input stream file ../data/ddia.figure8-4 output stream file dsljson/ddia.figure8-4.json
python3 ../pipes/pipe.py processor dsl2object.dsl_engine.DSL_Engine input stream file ../data/ddia.figure8-5 output stream file dsljson/ddia.figure8-5.json
python3 ../pipes/pipe.py processor timelines.timeline_engine.TimelineEngine input stream file dsljson/ddia.figure5-2.json output gist ddia.figure5-2.json output stream file ./dslgist/ddia.figure5-2.gist
python3 ../pipes/pipe.py processor timelines.timeline_engine.TimelineEngine input stream file dsljson/ddia.figure5-3.json output gist ddia.figure5-3.json output stream file ./dslgist/ddia.figure5-3.gist
python3 ../pipes/pipe.py processor timelines.timeline_engine.TimelineEngine input stream file dsljson/ddia.figure5-4.json output gist ddia.figure5-4.json output stream file ./dslgist/ddia.figure5-4.gist
python3 ../pipes/pipe.py processor timelines.timeline_engine.TimelineEngine input stream file dsljson/ddia.figure5-5.json output gist ddia.figure5-5.json output stream file ./dslgist/ddia.figure5-5.gist
python3 ../pipes/pipe.py processor timelines.timeline_engine.TimelineEngine input stream file dsljson/ddia.figure8-3.json output gist ddia.figure8-3.json output stream file ./dslgist/ddia.figure8-3.gist
python3 ../pipes/pipe.py processor timelines.timeline_engine.TimelineEngine input stream file dsljson/ddia.figure8-4.json output gist ddia.figure8-4.json output stream file ./dslgist/ddia.figure8-4.gist
python3 ../pipes/pipe.py processor timelines.timeline_engine.TimelineEngine input stream file dsljson/ddia.figure8-5.json output gist ddia.figure8-5.json output stream file ./dslgist/ddia.figure8-5.gist
