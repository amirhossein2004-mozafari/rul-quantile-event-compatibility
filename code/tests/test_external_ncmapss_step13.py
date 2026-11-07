"""Implementation tests only. Synthetic fixtures never enter experiment evidence."""
import importlib.util
from pathlib import Path
import h5py
import numpy as np
import pytest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('external13',ROOT/'scripts/external_ncmapss_step13.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

def test_fixed_schedule_uses_only_measured_first_window(tmp_path,monkeypatch):
    path=tmp_path/'synthetic_parser_fixture.h5'
    with h5py.File(path,'w') as h:
        h['W_var']=np.array([b'w0',b'w1',b'w2',b'w3']);h['X_s_var']=np.array([f's{i}'.encode() for i in range(14)])
        h['A_var']=np.array([b'unit',b'cycle',b'Fc',b'hs'])
        h['A_dev']=np.column_stack([np.ones(600),np.repeat([1,2],300),np.full(600,9999),np.full(600,9999)])
        h['Y_dev']=np.repeat([50.,49.],300).reshape(-1,1)
        h['W_dev']=np.arange(600*4).reshape(600,4).astype(float);h['X_s_dev']=np.zeros((600,14))
        h['X_v_dev']=np.full((600,2),9999.)
        # Test arrays deliberately absent: dev parsing cannot depend on them.
    monkeypatch.setattr(m,'DATA',path)
    d,meta=m.windows('dev')
    assert d['X'].shape==(2,30,18) and meta['features'][:4]==['w0','w1','w2','w3']
    np.testing.assert_array_equal(d['X'][0,:,0],np.arange(0,291,10)*4)
    np.testing.assert_array_equal(d['X'][1,:,0],np.arange(300,591,10)*4)
    np.testing.assert_array_equal(d['raw_y'],[50,49])

def test_analytic_scores_and_quantile_boundary():
    q=np.array([[10,20,25],[35,40,50],[10,40,50],[10,20,30]],float)
    y=np.array([15,45,60,30],float);logit=np.zeros(4)
    v,p=m.score_vectors(y,q,logit)
    np.testing.assert_allclose(v['distance'],[.45,.45,0,.45])
    np.testing.assert_allclose(v['Brier'],[.25]*4)
    np.testing.assert_allclose(v['Winkler'],[15,15,240,20])
    np.testing.assert_array_equal(v['coverage'],[1,1,0,1])

def test_evaluation_cannot_open_test_before_fit_freeze(tmp_path,monkeypatch):
    called=[]
    monkeypatch.setattr(m,'OUT',tmp_path);monkeypatch.setattr(m,'check_protocol',lambda:None)
    monkeypatch.setattr(m,'windows',lambda split:called.append(split))
    with pytest.raises(FileNotFoundError):m.evaluate()
    assert called==[]
