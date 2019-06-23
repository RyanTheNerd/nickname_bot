import requests
from PIL import Image

def deepfry(url):
    r = requests.get(url, allow_redirects=True)
    input_path = './frier/input/' + url.split('/')[-1].split('?')[0]
    open(input_path, 'wb').write(r.content)
    output_path = './frier/output/' + ''.join(input_path.split('/')[-1].split('.')[:-1]) + '.jpg';
    print()
    print('Deepfrying meme:')
    print(f'\tInput file: {input_path}')
    print(f'\tOutput file: {output_path}')

    im = Image.open(input_path).convert('RGB')
    ratio = im.height/im.width
    width = 500
    height = int(ratio * width)
    im = im.resize((width, height))
    im.save(output_path, format='JPEG', quality=7)
    return output_path



