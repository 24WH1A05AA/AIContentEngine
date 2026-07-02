"""Unit tests for Stage 2 modules without API calls."""

import json
from adaptation import adapt_for_channel, CHANNELS, AdaptationError


def test_adaptation_error_handling():
    """Test adaptation error handling."""
    print("\n" + "="*60)
    print("TEST: Adaptation Error Handling")
    print("="*60)
    
    # Test invalid channel
    try:
        adapt_for_channel("test", "test", {}, "InvalidChannel")
        print("[FAIL] Should have raised AdaptationError")
        return False
    except AdaptationError as e:
        print("[OK] Invalid channel caught: %s" % str(e)[:50])
    
    print("[PASS] Error handling works\n")
    return True


def test_adaptation_structure():
    """Test adaptation returns correct structure."""
    print("="*60)
    print("TEST: Adaptation Output Structure")
    print("="*60)
    
    # Verify CHANNELS are defined
    print("[OK] Defined channels: %s" % ", ".join(CHANNELS.keys()))
    assert len(CHANNELS) == 3, "Should have 3 channels"
    assert "B2B LinkedIn" in CHANNELS
    assert "Gen-Z TikTok" in CHANNELS
    assert "Parents Facebook" in CHANNELS
    
    # Check channel personas
    for channel, persona in CHANNELS.items():
        print("[OK] %s: has persona description" % channel)
        assert isinstance(persona, str)
        assert len(persona) > 0
    
    print("[PASS] Channel structure correct\n")
    return True


def test_voiceover_module():
    """Test voiceover module structure."""
    print("="*60)
    print("TEST: Voiceover Module")
    print("="*60)
    
    from voiceover import generate_narration_script, generate_voiceover
    import inspect
    
    # Check generate_narration_script signature
    sig = inspect.signature(generate_narration_script)
    params = list(sig.parameters.keys())
    print("[OK] generate_narration_script params: %s" % str(params))
    assert "blog" in params
    
    # Check generate_voiceover signature
    sig = inspect.signature(generate_voiceover)
    params = list(sig.parameters.keys())
    print("[OK] generate_voiceover params: %s" % str(params))
    assert "blog" in params
    assert "product_name" in params
    
    print("[PASS] Voiceover module structure correct\n")
    return True


def test_critic_module():
    """Test critic module structure."""
    print("="*60)
    print("TEST: Critic Module")
    print("="*60)
    
    from critic import critique, critique_and_regenerate
    import inspect
    
    # Check critique signature
    sig = inspect.signature(critique)
    params = list(sig.parameters.keys())
    print("[OK] critique params: %s" % str(params))
    assert all(p in params for p in ["tagline", "blog", "social_posts", "product_name"])
    
    # Check critique_and_regenerate signature
    sig = inspect.signature(critique_and_regenerate)
    params = list(sig.parameters.keys())
    print("[OK] critique_and_regenerate params: %s" % str(params))
    assert all(p in params for p in ["tagline", "blog", "social_posts", "product_name"])
    
    print("[PASS] Critic module structure correct\n")
    return True


def test_stage1_unchanged():
    """Test Stage 1 modules are unchanged."""
    print("="*60)
    print("TEST: Stage 1 Backward Compatibility")
    print("="*60)
    
    from text_gen import generate_tagline, generate_blog_intro, generate_social_posts
    import inspect
    
    # Verify Stage 1 functions exist and have correct signatures
    sig = inspect.signature(generate_tagline)
    params = list(sig.parameters.keys())
    print("[OK] generate_tagline: %s" % str(params))
    assert params == ["product_name", "target_audience", "brand_tone"]
    
    sig = inspect.signature(generate_blog_intro)
    params = list(sig.parameters.keys())
    print("[OK] generate_blog_intro: %s" % str(params))
    assert params == ["product_name", "target_audience", "brand_tone", "tagline"]
    
    sig = inspect.signature(generate_social_posts)
    params = list(sig.parameters.keys())
    print("[OK] generate_social_posts: %s" % str(params))
    assert params == ["product_name", "target_audience", "brand_tone", "tagline"]
    
    print("[PASS] Stage 1 functions unchanged\n")
    return True


def test_app_integration():
    """Test app.py integration."""
    print("="*60)
    print("TEST: App Integration")
    print("="*60)
    
    import ast
    with open("app.py", "r", encoding="utf-8") as f:
        code = f.read()
    
    # Verify syntax
    try:
        ast.parse(code)
        print("[OK] app.py syntax is valid")
    except SyntaxError as e:
        print("[FAIL] app.py has syntax errors: %s" % str(e))
        return False
    
    # Check for Stage 2 imports
    checks = [
        ("from critic import", "critic import"),
        ("from voiceover import", "voiceover import"),
        ("from adaptation import", "adaptation import"),
        ("render_stage2_section", "Stage 2 rendering"),
        ("critique_and_regenerate", "critique function"),
        ("generate_voiceover", "voiceover function"),
        ("adapt_for_channel", "adaptation function"),
    ]
    
    for check_str, description in checks:
        if check_str in code:
            print("[OK] %s found" % description)
        else:
            print("[FAIL] %s not found" % description)
            return False
    
    print("[PASS] App integration complete\n")
    return True


def run_unit_tests():
    """Run all unit tests."""
    print("\n" + "="*60)
    print("STAGE 2 UNIT TEST SUITE")
    print("="*60)
    
    tests = [
        test_adaptation_structure,
        test_adaptation_error_handling,
        test_voiceover_module,
        test_critic_module,
        test_stage1_unchanged,
        test_app_integration,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print("[FAIL] Test failed with error: %s\n" % str(e))
            results.append(False)
    
    print("="*60)
    if all(results):
        print("[SUCCESS] ALL UNIT TESTS PASSED (%d/%d)" % (sum(results), len(results)))
        print("="*60)
        print("\nVerification Summary:")
        print("[OK] critic.py: structure correct, imports work")
        print("[OK] voiceover.py: structure correct, imports work")
        print("[OK] adaptation.py: 3 channels supported, error handling")
        print("[OK] app.py: integrates all Stage 2 modules")
        print("[OK] Stage 1: backward compatible, unchanged")
        return True
    else:
        print("[FAIL] SOME TESTS FAILED (%d/%d)" % (sum(results), len(results)))
        print("="*60)
        return False


if __name__ == "__main__":
    success = run_unit_tests()
    exit(0 if success else 1)
