<div align="center">
<h1>Ai Anime Arena</h1>

**English** | [日本語](Docs/README_ja.md)

https://github.com/user-attachments/assets/318d79c2-3438-440f-aeb0-7ac8d2ec2f95


<a href="https://evaluate.sh" rel="dofollow"><strong>Explore the Web »</strong></a>
</div>

AI-Anime-Arena is an anime art benchmark platform featuring anonymous and randomized battles. All the code in this repository is hosted at [https://evaluate.sh](https://evaluate.sh).

> [!IMPORTANT]
> Currently in beta; this project may be terminated without notice.


## Features
- **Limited to Anime-Style Images**: We evaluate models used solely for anime-style artwork, not those designed to generate photorealistic or realistic images.
- **Multilingual and Cross-Lingual Support**: Simply copy multilingual text and paste it into the input box. No need to worry about the language.
- **Comparison Including Workflows**: We focus on integrated workflows that include not only pure model comparisons but also LoRA, prompt control, etc.
- **Accepting Requests**: You can request to add models to this repository.

## Request to Add Workflows
- Please create a repository that meets the following requirements and submit a request via [issues](https://github.com/S-Tubasa/AI-Anime-Arena/issues).
  - After verification, it will be automatically linked as a submodule to this repository.
- If you do not wish to make it public, you can also send a tarball or private repository to [email](5andw1ch001@proton.me).
  - In that case, it will not be linked as a submodule to the repository.

### Requirements
- It must be an architecture that uses models focused on anime-style artwork, not designed to generate photorealistic or realistic images.
- Generation must be possible with a Python script in the form `python main.py --mode 1or2 --prompt "XXXXXX" --save_path "XXXX.webp"`.
  - `mode`: Specify the image size as 1 or 2
    - 1: Aspect ratio of 3:2 (768x512, 1824x1248, etc.)
    - 2: Aspect ratio of 2:3 (512x768, 1248x1824, etc.)
  - `prompt`: The text used for generation
    - Strongly recommend English as it will be automatically translated within the server
  - `save_path`: The path to save the image
    - Recommend including the extension, preferably PNG, JPG, or WEBP
- Setup instructions must be clearly stated.
  - For how to write, please refer to [this repository](https://github.com/S-Tubasa/Animagine_XL_3_1_Basic).
- **Important**: Inference speed must be within around 20seconds on a graphics card equivalent to RTX 4090.
  - Including loading time due to model size, it must be within around 20 seconds.

## Data Usage
- Currently under preparation

## Disclaimer

- All code and datasets are released under the CC BY-SA 4.0 license. For details, please refer to [LICENSE](LICENSE).
  - However, regarding the generated images within the dataset, please comply with each model's license.
- Please refer to the laws of your region regarding DMCA and other relevant laws.
