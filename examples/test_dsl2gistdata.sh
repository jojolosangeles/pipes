set -x
rm -rf ./examples/dsljson
rm -rf ./examples/gistdata
mkdir ./examples/dsljson
mkdir ./examples/gistdata
python3 pipeit.py processor dsl2object.dsl_engine.DSL_Engine input stream file data/ddia.figure5-2 output stream file examples/dsljson/ddia.figure5-2.json
python3 pipeit.py processor dsl2object.dsl_engine.DSL_Engine input stream file data/ddia.figure5-3 output stream file examples/dsljson/ddia.figure5-3.json
python3 pipeit.py processor dsl2object.dsl_engine.DSL_Engine input stream file data/ddia.figure5-4 output stream file examples/dsljson/ddia.figure5-4.json
python3 pipeit.py processor dsl2object.dsl_engine.DSL_Engine input stream file data/ddia.figure5-5 output stream file examples/dsljson/ddia.figure5-5.json
python3 pipeit.py processor dsl2object.dsl_engine.DSL_Engine input stream file data/ddia.figure8-3 output stream file examples/dsljson/ddia.figure8-3.json
python3 pipeit.py processor dsl2object.dsl_engine.DSL_Engine input stream file data/ddia.figure8-4 output stream file examples/dsljson/ddia.figure8-4.json
python3 pipeit.py processor dsl2object.dsl_engine.DSL_Engine input stream file data/ddia.figure8-5 output stream file examples/dsljson/ddia.figure8-5.json
python3 pipeit.py processor timelines.timeline_engine.TimelineEngine input stream file examples/dsljson/ddia.figure5-2.json output stream file examples/gistdata/ddia.figure5-2.json
python3 pipeit.py processor timelines.timeline_engine.TimelineEngine input stream file examples/dsljson/ddia.figure5-3.json output stream file examples/gistdata/ddia.figure5-3.json
python3 pipeit.py processor timelines.timeline_engine.TimelineEngine input stream file examples/dsljson/ddia.figure5-4.json output stream file examples/gistdata/ddia.figure5-4.json
python3 pipeit.py processor timelines.timeline_engine.TimelineEngine input stream file examples/dsljson/ddia.figure5-5.json output stream file examples/gistdata/ddia.figure5-5.json
python3 pipeit.py processor timelines.timeline_engine.TimelineEngine input stream file examples/dsljson/ddia.figure8-3.json output stream file examples/gistdata/ddia.figure8-3.json
python3 pipeit.py processor timelines.timeline_engine.TimelineEngine input stream file examples/dsljson/ddia.figure8-4.json output stream file examples/gistdata/ddia.figure8-4.json
python3 pipeit.py processor timelines.timeline_engine.TimelineEngine input stream file examples/dsljson/ddia.figure8-5.json output stream file examples/gistdata/ddia.figure8-5.json
