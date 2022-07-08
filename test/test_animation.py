from viztools import Animation
import os 

def test_animation():
    if not os.path.exists('/tmp/animation'):
        os.mkdir('/tmp/animation')
    video = Animation(
        region='kc_mo',
        start='2022-07-01T00:00:00Z',
        end='2022-01-07T00:00:00Z',
        zoom=11
    )
    video.create_animation(dirname='/tmp/animation', fps=1)

if __name__ == '__main__':
    test_animation()