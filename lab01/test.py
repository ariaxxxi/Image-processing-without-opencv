#!/usr/bin/env python3

import os
import pickle
import hashlib

import lab
import pytest

TEST_DIRECTORY = os.path.dirname(__file__)


def object_hash(x):
    return hashlib.sha512(pickle.dumps(x)).hexdigest()


def compare_images(im1, im2):
    assert set(im1.keys()) == {'height', 'width', 'pixels'}, 'Incorrect keys in dictionary'
    assert im1['height'] == im2['height'], 'Heights must match'
    assert im1['width'] == im2['width'], 'Widths must match'
    assert len(im1['pixels']) == im1['height']*im1['width'], 'Incorrect number of pixels'
    assert all(isinstance(i, int) for i in im1['pixels']), 'Pixels must all be integers'
    assert all(0<=i<=255 for i in im1['pixels']), 'Pixels must all be in the range from [0, 255]'
    pix_incorrect = (None, None)
    for ix, (i, j) in enumerate(zip(im1['pixels'], im2['pixels'])):
        if i != j:
            pix_incorrect = (ix, abs(i-j))
    assert pix_incorrect == (None, None), 'Pixels must match.  Incorrect value at location %s (differs from expected by %s)' % pix_incorrect



def test_load():
    result = lab.load_image(os.path.join(TEST_DIRECTORY, 'test_images', 'centered_pixel.png'))
    expected = {
        'height': 11,
        'width': 11,
        'pixels': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 255, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    }
    compare_images(result, expected)


def test_inverted_1():
    im = lab.load_image(os.path.join(TEST_DIRECTORY, 'test_images', 'centered_pixel.png'))
    result = lab.inverted(im)
    expected = {
        'height': 11,
        'width': 11,
        'pixels': [255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                   255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                   255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                   255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                   255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                   255, 255, 255, 255, 255, 0, 255, 255, 255, 255, 255,
                   255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                   255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                   255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                   255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                   255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255],
    }
    compare_images(result, expected)

def test_inverted_2():
    result = lab.load_image(os.path.join(TEST_DIRECTORY, 'test_images', 'centered_pixel.png'))
    expected = {
        'height': 1,
        'width': 4,
        'pixels': [230, 160, 105, 41],
    }
    compare_images(result, expected)
    assert False


def invert_filter():
    inpfile = lab.load_image(os.path.join(TEST_DIRECTORY, 'test_images', 'bluegill.png'))
    im = lab.load_image(inpfile)
    #oim = test.object_hash(im)
    result = lab.inverted(im)
    lab.save_image(result, 'bluegill_inverted', mode='PNG')


@pytest.mark.parametrize("fname", ['mushroom', 'twocats', 'chess'])
def test_inverted_images(fname):
    inpfile = os.path.join(TEST_DIRECTORY, 'test_images', '%s.png' % fname)
    expfile = os.path.join(TEST_DIRECTORY, 'test_results', '%s_invert.png' % fname)
    im = lab.load_image(inpfile)
    oim = object_hash(im)
    result = lab.inverted(im)
    expected = lab.load_image(expfile)
    assert object_hash(im) == oim, 'Be careful not to modify the original image!'
    compare_images(result, expected)


@pytest.mark.parametrize("kernsize", [1, 3, 7])
@pytest.mark.parametrize("fname", ['mushroom', 'twocats', 'chess'])
def test_blurred_images(kernsize, fname):
    inpfile = os.path.join(TEST_DIRECTORY, 'test_images', '%s.png' % fname)
    expfile = os.path.join(TEST_DIRECTORY, 'test_results', '%s_blur_%02d.png' % (fname, kernsize))
    input_img = lab.load_image(inpfile)
    input_hash = object_hash(input_img)
    result = lab.blurred(input_img, kernsize)
    expected = lab.load_image(expfile)
    assert object_hash(input_img) == input_hash, "Be careful not to modify the original image!"
    compare_images(result, expected)

def test_blurred_black_image():
    # REPLACE THIS with your 1st test case from section 6.1
    assert False

def test_blurred_centered_pixel():
    # REPLACE THIS with your 2nd test case from section 6.1
    assert False

@pytest.mark.parametrize("kernsize", [1, 3, 9])
@pytest.mark.parametrize("fname", ['mushroom', 'twocats', 'chess'])
def test_sharpened_images(kernsize, fname):
    inpfile = os.path.join(TEST_DIRECTORY, 'test_images', '%s.png' % fname)
    expfile = os.path.join(TEST_DIRECTORY, 'test_results', '%s_sharp_%02d.png' % (fname, kernsize))
    input_img = lab.load_image(inpfile)
    input_hash = object_hash(input_img)
    result = lab.sharpened(input_img, kernsize)
    expected = lab.load_image(expfile)
    assert object_hash(input_img) == input_hash, "Be careful not to modify the original image!"
    compare_images(result, expected)


@pytest.mark.parametrize("fname", ['mushroom', 'twocats', 'chess'])
def test_edges_images(fname):
    inpfile = os.path.join(TEST_DIRECTORY, 'test_images', '%s.png' % fname)
    expfile = os.path.join(TEST_DIRECTORY, 'test_results', '%s_edges.png' % fname)
    input_img = lab.load_image(inpfile)
    input_hash = object_hash(input_img)
    result = lab.edges(input_img)
    expected = lab.load_image(expfile)
    assert object_hash(input_img) == input_hash, "Be careful not to modify the original image!"
    compare_images(result, expected)

def test_edges_centered_pixel():
    # REPLACE THIS with your test case from section 7
    assert False

if __name__ == '__main__':
    import os
    import sys
    import json
    import pickle
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--gather", action='store_true')
    parser.add_argument("--server", action='store_true')
    parser.add_argument("--initial", action='store_true')
    parser.add_argument("args", nargs="*")

    parsed = parser.parse_args()

    class TestData:
        def __init__(self, gather=False):
            self.alltests = None
            self.results = {'passed': []}
            self.gather = gather

        @pytest.hookimpl(hookwrapper=True)
        def pytest_runtestloop(self, session):
            yield

        def pytest_runtest_logreport(self, report):
            if report.when != 'call':
                return
            self.results.setdefault(report.outcome, []).append(report.head_line)

        def pytest_collection_finish(self, session):
            if self.gather:
                self.alltests = [i.name for i in session.items]


    pytest_args = ['-v', __file__]

    if parsed.server:
        pytest_args.insert(0, '--color=yes')

    if parsed.gather:
        pytest_args.insert(0, '--collect-only')

    testinfo = TestData(parsed.gather)
    res = pytest.main(
        ['-k', ' or '.join(parsed.args), *pytest_args],
        **{'plugins': [testinfo]}
    )

    if parsed.server:
        _dir = os.path.dirname(__file__)
        if parsed.gather:
            with open(os.path.join(_dir, 'alltests.json'), 'w' if parsed.initial else 'a') as f:
                f.write(json.dumps(testinfo.alltests))
                f.write('\n')
        else:
            with open(os.path.join(_dir, 'results.json'), 'w' if parsed.initial else 'a') as f:
                f.write(json.dumps(testinfo.results))
                f.write('\n')
