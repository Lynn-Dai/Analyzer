# Dependency Facade: The Coupling and Conflicts between Android Framework and Its Customization

## Methodology
This directory contains the executable tools and scripts to analyze source code and history and implement experiments.

### The detection of Dependency facade

#### Entity and Dependency Extraction

- `enre_java.jar` -
- input:
- command:
- output:
    
#### Entity Ownership Identification
- jar or scripts
- input
- command
- output
  - `all_base_commits.csv` - the evolution history of all commits of the upstream AOSP frameworks/base
  - `<project name>-<version>-ownership.xlsx` - the final collection of all project versions' entity ownership detection results
  - `<project name>-<version>`
    - blame_dict.csv - git blame detection result of current project selected merge node 
    - accompany_commits.csv - information of current project version's commit history
    - base_commits.csv - information of merge point which downstream project version merging upstream AOSP
    - old_base_commits.csv - commit history of current project version which belongs to upstream AOSP old version
    - only_accompany_commits.csv - commit history of current project version which belongs to downstream project
    - all_entities.csv - all entities and commits which contributed to specific entity information of files which contains intrusive modification of downstream project
    - final_ownership.csv - the entity ownership detection result below the 'File' level in the project
    - final_ownership_file_count.csv - the number of each kind of entity combined with ownership detection result for all files of current project version

#### Intrusive Operation Identification
  This directory contains the data of different kinds of intrusive modification, following diagram shows the detail of each file.
- jar or scripts
- input
- command
- output:
  - `intrusive.xlsx` - The collection of different kinds of intrusive modification's quantity for all project version
  - `<project name>-<version>`
    - intrusive_file_count.csv - The quantity of each kind of intrusive modification which is counted in files

#### Dependency facade output:
- `facade.xlsx` - the collection of all downstream project versions' dependency facade detection results
- `<project name>-<version>`
  - facade.json - the detection result of dependency facade of current project version
  - facade_file_filter.csv - The number of each kind of entity appearing in the dependency facade which is counted in files

### Restriction Level Labeling
- command
- non-SDK restriction files (hiddenapi-flags.csv)
This directory contains data of non-SDK restriction files and the matching statistics, following diagram shows the details.
  - `matching.xlsx` - the matching statistics of non-SDK restriction files to dependency graph which is provided by ENRE
  - `hiddenapi-flags-<project name>-<version>.csv` - the 'hiddenapi-flags.csv' of downstream LineageOS 18.1 and 19.1, upstream AOSP 11 and 12. 

## Set up
This directory contains the preliminary data to conduct following experiments and study our four research questions.

### Subject and Version Collection

### Merge Conflict Collection
This directory contains data of textual conflicts detection results of each project versions and details of manually selected conflict blocks.

- `<project name>-<version>-merge.csv` - the conflict details of current downstream project version which contains merge nodes, conflict files quantity, conflict java files quantity and conflict blocks LOC.

## Results
### RQ1: How do the downstream customizations rely on the upstream Android through interface-level dependencies?

- entity ownership distribution
- facade size measurements
- interface-level dependencies (D->U)
- top packages

### RQ2: How do the downstream customizations rely on the upstream Android through intrusion-level dependencies?

- intrusive operations
- reverse dependencies
- hotspot upstream entities

### RQ3: How do the downstream customizations adapt to the dependency constraint imposed by the upstream Android?

- state transform
- industrial modification
- non-SDK API usage

### RQ4: How do merge conflicts occur on the dependency facade between downstream customizations and the upstream Android?

- conflict blocks on the dependency facade
- `selected-conf-block.docx` - the selected conflict blocks details.

# Threats

First, our DepFCD employs the ENRE [21–23] for entity and dependency extraction. It supports extracting possible dependencies caused by dynamic features, which other tools failed to identify [21, 23]. Second, the accuracy of Entity Ownership Identification and Intrusive Operation Identification of our DepFCD would impact the study of RQ1 and RQ2. To reduce threats, we combined the git blame command [6] and
advanced RefactoringMiner [38, 45, 46] for an accurate analysis of commit history. git blame [6] traces code modifications and RefactoringMiner identify refactoring operations involved in modifications. RefactoringMiner has been widely adopted in diverse work [20, 24, 40, 47].

Our RQ3 employed the Restriction Level Labeling of DepFCD to assign the non-SDK restriction levels documented in “hiddenapi.csv” into the corresponding entities. To mitigate possible threats, we fetched and compiled the entire huge-scale
project repositories to generate accurate “hiddenapi.csv” files.

Our RQ4 conducted a manual study on the code conflicts on the dependency facade. To mitigate the possible subjectivity, the two authors of this work independently analyzed the conflict cases and reached consistent results. Moreover, we
reported the results on IndustrialX to its developers. They confirmed our observations on these cases, as discussed in Section V. We will analyze more conflict cases.

