from warped_contract import ROOT
from audit_saved_triangles_v2 import inspect

def test_serialized_base_contains_support_and_no_sampled_obstruction():
    s=inspect(ROOT/'V2_WARPED_STAIRS_BASE.glb')
    assert s['mesh_count']==293
    assert s['body_collision_sample_count']==0
    assert s['supported_stair_treads']==s['tested_stair_treads']==8

def test_serialized_blocker_is_detected():
    s=inspect(ROOT/'V2_NEGATIVE_STAIR_BLOCK.glb')
    assert s['body_collision_sample_count']>0
    assert 'NEGATIVE_BLOCKED_HEADSPACE' in s['collision_parts']

def test_serialized_missing_step_is_detected():
    s=inspect(ROOT/'V2_NEGATIVE_MISSING_TREAD.glb')
    assert s['body_collision_sample_count']==0
    assert s['supported_stair_treads']==7

def test_serialized_market_counterfactual_still_has_stair_support():
    s=inspect(ROOT/'V2_MUTATED_MARKET.glb')
    assert s['body_collision_sample_count']==0 and s['supported_stair_treads']==8
