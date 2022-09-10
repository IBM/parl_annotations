# parl_annotations
* defines abstract class for planning annotation reinforcement learning.

## Install
```
conda create -n parl_minigrid python=3.7
conda activate parl_minigrid
pip install -r requirements
pip install -e .
```

# Citations
```
@inproceedings{lee2021ai,
  title={AI Planning Annotation in Reinforcement Learning: Options and Beyond},
  author={Lee, Junkyu and Katz, Michael and Agravante, Don Joven and Liu, Miao and Klinger, Tim and Campbell, Murray and Sohrabi, Shirin and Tesauro, Gerald},
  booktitle={Planning and Reinforcement Learning PRL Workshop at ICAPS},
  year={2021}
}
```

# License
Apache-2.0 License


# Referencces
This project utilizes the following opensource projects.
* `pyperplan`
* `fastdownward`
```
@Misc{alkhazraji-et-al-zenodo2020,
  author =       "Yusra Alkhazraji and Matthias Frorath and Markus Gr{\"u}tzner
                  and Malte Helmert and Thomas Liebetraut and Robert Mattm{\"u}ller
                  and Manuela Ortlieb and Jendrik Seipp and Tobias Springenberg and
                  Philip Stahl and Jan W{\"u}lfing",
  title =        "Pyperplan",
  publisher =    "Zenodo",
  year =         "2020",
  doi =          "10.5281/zenodo.3700819",
  url =          "https://doi.org/10.5281/zenodo.3700819",
  howpublished = "\url{https://doi.org/10.5281/zenodo.3700819}"
}

@article{helmert2006fast,
  title={The Fast Downward planning system.},
  author={Helmert, Malte},
  journal={Journal of Artificial Intelligence Research},
  volume={26},
  pages={191--246},
  year={2006}
}

```
