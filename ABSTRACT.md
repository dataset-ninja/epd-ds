The authors collected a high-resolution remote sensing image **EPD: Electric Pylon Detection Dataset** for electric pylon detection (EPD). Images in the EPD dataset were collected from Google Earth and image productions of Pleiades satellite. Specially, all images in the dataset are processed multi-spectral remote sensing image products, which are widely used in practical detection tasks. 

## Motivation

Electricity stands as a cornerstone for economic advancement and technological strides. Ensuring a stable electricity supply is pivotal for regional progress. Within the entire power infrastructure, the electric network assumes a crucial role in transferring energy from centrally located power plants to widely dispersed individual users. Essentially, this segment of the power system is closely intertwined with urban power provision. Regular monitoring of electric pylons, which serve to support and guide wires, is essential to maintain operational integrity. However, as electricity becomes more ubiquitous and electric networks grow in complexity, residential areas exhibit a trend towards expansion and diversification. Given the current landscape of electric pylon distribution, characterized by numerous pylons spanning vast distances, varying appearances, and intricate terrain, traditional manual field inspections demand considerable resources while yielding limited efficiency. Utilizing unmanned aerial vehicles (UAVs) for field inspections may offer improved performance. Nonetheless, this method struggles to meet real-time monitoring demands over extensive areas and remains susceptible to interference from surrounding tall structures. In contrast, satellite remote sensing offers a broader monitoring scope and proves to be efficient while being less influenced by surrounding factors. This technology, commonly employed in global environmental observation, presents a viable solution for electric network monitoring.

Moreover, the manual interpretation of high-resolution remote sensing images demands considerable effort. Despite this, in addition to the challenges posed by the characteristics of electric pylons themselves, manual interpretation suffers from inherent limitations compared to machine recognition, namely visual fatigue. Continuous manual interpretation work can significantly diminish efficiency and accuracy due to the effects of visual fatigue. In recent years, there has been a surge of interest in target detection methods based on deep learning within related fields. These methods have proven effective in detecting various objects such as aircraft, ships, and cooling towers, supported by numerous successful experiments. Furthermore, deep-learning-based detectors demonstrate versatility across multiple remote sensing data sources, including optical, infrared, LiDAR, and SAR, as well as aerial images. As deep learning theory continues to advance and detection algorithms undergo iterative updates, deep learning-based target detectors exhibit superiority over traditional object detection methods.

## Dataset description

In their exploration of electric pylon detection using deep learning techniques, the authors undertook a meticulous effort to curate a high-resolution remote sensing image dataset specifically tailored for this purpose, termed the Electric Pylon Detection (EPD) dataset. The images comprising this dataset were sourced from both Google Earth and the image archives of the Pleiades satellite. Notably, all images within the EPD dataset are processed multi-spectral remote sensing products, commonly employed in practical detection tasks. The Pleiades images are orthoimages, while those obtained from Google Earth represent multi-spectral products captured by various sensors. This integration of data from multiple sources serves to enhance the testing of the generalization capabilities of deep learning detectors.

<img src="https://github.com/dataset-ninja/epd-ds/assets/120389559/9e5b2384-98c3-41d5-b43e-536fc29f7389" alt="image" width="1000">

<span style="font-size: smaller; font-style: italic;">Image samples in the EPD dataset. The first and second images were captured by Pleiades satellite, while the third image and fourth images were collected from Google Earth. All image samples in the dataset were obtained from these two sources and image formats are all processed multi-spectral image products.</span>

The detection of electric pylons in high-resolution optical remote sensing images presents a myriad of challenges due to the diverse features exhibited by these targets. Firstly, the widespread deployment of pylons results in significant variations in size and specifications. Even within the same spatial resolution, the area occupied by different pylons within an image may vary considerably. Additionally, the background environment surrounding pylons varies greatly due to the extensive coverage of the power network. Factors such as lighting conditions and topography further influence the characteristics of electric pylons. Lighting conditions impact the color appearance of pylons, while topography affects the tilt angle of pylons relative to the observation angle of satellites.

To assess the adaptability of various detectors to these influencing factors, the authors meticulously selected electric pylon targets in different states when constructing their dataset. The Electric Pylon Detection (EPD) dataset comprises a total of 1500 images, with 720 images captured by the Pleiades satellite along the Huimao Line in Guangdong Province, China—a major power network route in southern China. The remaining images were sourced from Google Earth to broaden the dataset's representativeness. The spatial resolution of images in the EPD dataset is 1 meter per pixel. Furthermore, to thoroughly evaluate the detectors' adaptability in real-world scenarios, the authors curated a subset of 50 relatively complex images from the EPD dataset, designated as ***epd-c***. This subset includes 20 images from the Pleiades satellite and 30 images from Google Earth. Selection criteria for images in ***epd-c*** include background interference, such as the presence of similar features or interfering objects, as well as the unique characteristics or varying scales of the targets to be detected.

| Features and Background       | Number of Images | Number of Targets |
|-------------------------------|------------------|-------------------|
| 20 Images from Pleiades Satellite |                 |                   |
| green fields                  |         2        |        8          |
| multicolored fields           |         2        |        5          |
| mountains                     |         2        |        2          |
| towns + multicolored fields   |         2        |        4          |
| towns + mountains             |         4        |        6          |
| mountains + multicolored fields |       2        |        3          |
| lakes                         |         2        |        6          |
| complex terrain               |         4        |        4          |

| 30 Images from Google Earth   |                 |                   |
| frame architectures           |         6        |       32          |
| multicolored fields           |         6        |       14          |
| shadows                       |         1        |        2          |
| highways                      |         2        |        5          |
| special electric pylons      |         3        |        8          |
| small targets                 |         4        |       27          |
| large size variation          |         2        |       18          |
| complex terrain               |         6        |       15          |

<span style="font-size: smaller; font-style: italic;">Details of the complex test subset EPD-C.</span>

Apart from the inherent characteristics of electric pylons, the surrounding background presents additional challenges to the detection task, notably in terms of background color and interference from surrounding objects. The light-colored frame structure of electric pylons can lead to significant interference with detection results, particularly when juxtaposed against light backgrounds and frame structure buildings. Specifically, the authors designate the remaining 1450 images in the EPD dataset, excluding those in ***epd-c***, as a standard subset named ***epd-c***. This subset encompasses more than 3000 electric pylons and serves as the basis for training detectors and conducting random experiments.

<img src="https://github.com/dataset-ninja/epd-ds/assets/120389559/953aee76-e818-4f62-8ae0-12c00d7cac8b" alt="image" width="800">

<span style="font-size: smaller; font-style: italic;">Image samples in the complex test subset EPD-C. The left one was captured by Pleiades satellite, where the detection difficulty mainly lies in the similarity of color characteristics between the background and electric pylon targets. The right one was collected from Google Earth, where the detection difficulty mainly reflects on interference from frame structure buildings.</span>


