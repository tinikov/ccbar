# Data process workflow (ccbar)

## 0. Prerequisites

- **Directory structure**:   
(general)
```
.
├── bin
├── data
├── corr2-eff.sh
├── FKS-TD.sh
├── FKS-TI.sh
├── M-fit.py
├── pre.sh
├── pre2.sh
└── pre4.sh
```

- **Directory structure of `data`**:   
(Correlators here should be averaged over different source points)
```
.
└── raw
    ├── c2pt
    │   ├── av
    │   ├── ps
    │   ├── s
    │   ├── t
    │   └── v
    ├── c4pt
    │   ├── ps (00 - 63 inside)
    │   └── v  (00 - 63 inside)
    ├── l2pt
    │   ├── av
    │   ├── ps
    │   ├── s
    │   ├── t
    │   └── v
    └── l4pt
        ├── ps (00 - 63 inside)
        └── v  (00 - 63 inside)
```

## 1. Pre-Process

|  |  |
| ------- | ------- |
| **RUN** | `./pre.sh` |
| **HINT** | Modify the *temporal and spacial length* in `./pre.sh` |

**OUTPUT**: 
- 2-point: in `data/x2pt/jsample`.  
Jackknife resampled data *(real part with arithmetic variance)* 
- 4-point: in `data/x4pt/jsample`.  
Jackknife resampled data *(real part with arithmetic variance)* 

## 2. Correlator (2-point)
### 2.1 Finalization: Correlator and Effective Mass

|  |  |
| ------- | ------- |
| **RUN** | `corr2-eff.sh` |
| **HINT** | Modify the *temporal and spacial length* in `./pre.sh` |
| **OUTPUT** | *Jackknife resampled data* in `data/xxpt/jsample`. |

- Run `eff-corr2.sh`. The result will be saved in `result/x2pt/corr` and `result/x2pt/effmass`
- Run `M-fit.py`. The result will be saved in `result/x2pt`

## 3. Correlator (4-point)

- Run `corr4.sh`. The result will be saved in `result/x4pt/corr` and `result/x4pt/effmass`

## 4. Time-independent Kawanai-Sasaki

## 5. Time-dependent Kawanai-Sasaki
### 5.1 Standard procedure

- Run `./FKS-TD.sh`. Result of Kawanai-Sasaki function will be in `result/x4pt/FKS-TD`;
- Fit the 
