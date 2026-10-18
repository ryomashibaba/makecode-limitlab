# P2.1 synthetic transcript

`p21_synthetic.csv` is generated entirely by the offline JavaScript VM in
`tests/test_p21.js`, using a 35×33×34 mock world and a mock player at 0,0,0.
It contains no Minecraft hardware measurements, private world coordinates,
user CSV, or local filesystem paths. The VM test compares its live output
against this fixture. Python CSV mutation tests read it without requiring
Node or compiled MakeCode, so the repository-wide Python suite works alone.
