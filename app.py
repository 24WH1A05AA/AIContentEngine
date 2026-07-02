"""AI Content Engine - Streamlit application for marketing campaign generation."""

import streamlit as st
from typing import Optional, Dict

# Page configuration must happen before any other st calls
st.set_page_config(
    page_title="AI Content Engine",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Catch missing API key errors at import time and show a friendly message
try:
    from config import OPENROUTER_API_KEY, HF_API_KEY
except Exception as _cfg_error:
    st.error(f"❌ Configuration error: {_cfg_error}")
    st.stop()

from text_gen import generate_tagline, generate_blog_intro, generate_social_posts, TextAPIError
from image_gen import generate_image, MediaAPIError as ImageAPIError
from video_gen import generate_video, MediaAPIError as VideoAPIError
from critic import critique_and_regenerate
from voiceover import generate_voiceover, VoiceoverError
from adaptation import adapt_for_channel, AdaptationError
from utils import format_download_content, validate_inputs, format_filename

# Custom CSS
CUSTOM_CSS = """
<style>
.main-header {
    font-size: 2.5rem;
    font-weight: 700;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
}
.subtitle {
    font-size: 1.1rem;
    color: #666;
    margin-bottom: 2rem;
}
.section-heading {
    font-size: 1.3rem;
    font-weight: 600;
    color: #667eea;
    margin-top: 1.5rem;
    margin-bottom: 1rem;
}
</style>
"""


def render_sidebar() -> None:
    """Render sidebar with branding and instructions."""
    with st.sidebar:
        st.markdown("## 🚀 AI Content Engine")
        st.markdown("---")
        st.markdown(
            """
        **Transform your product brief into a complete marketing campaign in seconds.**

        ✨ Generate:
        - Campaign Tagline
        - 200-word Blog
        - Social Posts
        - Hero Image
        - Promo Video
        """
        )
        st.markdown("---")
        st.info("💡 Fill in your product details and click Generate to create your campaign.")


def render_header() -> None:
    """Render main header with gradient text."""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    st.markdown(
        """
    <div class="main-header">🚀 AI Content Engine</div>
    <div class="subtitle">Generate your entire marketing campaign from a single brief</div>
    """,
        unsafe_allow_html=True,
    )


def validate_api_keys() -> None:
    """Check for missing API keys and stop if any are missing."""
    errors = []
    if not OPENROUTER_API_KEY:
        errors.append("❌ **OPENROUTER_API_KEY** is missing — required for text generation (tagline, blog, social posts)")
    
    # HF_API_KEY is optional but recommended for better video generation performance
    if not HF_API_KEY:
        st.warning("⚠️ **HF_API_KEY** is optional but recommended for video generation. Get a free token at https://huggingface.co/settings/tokens")

    if errors:
        for error in errors:
            st.error(error)
        st.info("Please add the missing keys to your .env file and restart the app.")
        st.stop()


def render_input_section() -> tuple[str, str, str]:
    """Render input section and return form values."""
    st.markdown(
        '<div class="section-heading">📋 Campaign Details</div>',
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3, gap="medium")

    with col1:
        product_name = st.text_input(
            "Product Name",
            placeholder="e.g., EcoBottle",
            label_visibility="collapsed",
        )

    with col2:
        target_audience = st.text_input(
            "Target Audience",
            placeholder="e.g., Eco-conscious millennials",
            label_visibility="collapsed",
        )

    with col3:
        brand_tone = st.selectbox(
            "Brand Tone",
            ["eco", "premium", "playful"],
            label_visibility="collapsed",
        )

    st.markdown("---")
    return product_name, target_audience, brand_tone


def generate_campaign(
    product_name: str, target_audience: str, brand_tone: str, left_col, right_col
) -> Optional[Dict]:
    """
    Generate all campaign assets.

    Args:
        product_name: Name of the product
        target_audience: Target audience
        brand_tone: Brand tone
        left_col: Left column for text content
        right_col: Right column for media

    Returns:
        Dictionary with generated assets or None on failure
    """
    progress_bar = st.progress(0)
    status_text = st.empty()

    try:
        # Step 1: Tagline
        status_text.info("⏳ Step 1/5: Generating tagline...")
        progress_bar.progress(0.2)
        with left_col:
            with st.spinner("🎯 Creating tagline..."):
                tagline = generate_tagline(product_name, target_audience, brand_tone)
                with st.container(border=True):
                    st.markdown(
                        '<div class="section-heading">✨ Tagline</div>',
                        unsafe_allow_html=True,
                    )
                    st.write(tagline)

        # Step 2: Blog
        status_text.info("⏳ Step 2/5: Generating blog introduction...")
        progress_bar.progress(0.4)
        with left_col:
            with st.spinner("📝 Creating blog..."):
                blog = generate_blog_intro(
                    product_name, target_audience, brand_tone, tagline
                )
                with st.container(border=True):
                    st.markdown(
                        '<div class="section-heading">📝 Blog Introduction</div>',
                        unsafe_allow_html=True,
                    )
                    st.write(blog)

        # Step 3: Social Posts
        status_text.info("⏳ Step 3/5: Generating social media posts...")
        progress_bar.progress(0.6)
        with left_col:
            with st.spinner("📱 Creating social posts..."):
                social_posts = generate_social_posts(
                    product_name, target_audience, brand_tone, tagline
                )
                with st.container(border=True):
                    st.markdown(
                        '<div class="section-heading">📱 Social Media Posts</div>',
                        unsafe_allow_html=True,
                    )
                    st.markdown("**🐦 Twitter:**")
                    st.write(social_posts["twitter"])
                    st.markdown("**📷 Instagram:**")
                    st.write(social_posts["instagram"])
                    st.markdown("**💼 LinkedIn:**")
                    st.write(social_posts["linkedin"])

        # Step 3.5: Critic
        status_text.info("⏳ Step 3.5/5: Running AI self-critique...")
        progress_bar.progress(0.65)
        critique_report = None
        try:
            with left_col:
                with st.spinner("🤖 Evaluating content..."):
                    critique_report = critique_and_regenerate(
                        tagline, blog, social_posts, product_name, target_audience, brand_tone
                    )
                    tagline = critique_report["tagline"]["content"]
                    blog = critique_report["blog"]["content"]
                    social_posts = critique_report["social"]["content"]
                    
                    # Show critique results
                    with st.container(border=True):
                        st.markdown(
                            '<div class="section-heading">🤖 AI Self-Critique</div>',
                            unsafe_allow_html=True,
                        )
                        col_tagline, col_blog, col_social = st.columns(3)
                        with col_tagline:
                            status = "✅ PASS" if critique_report["tagline"]["pass"] else "⚠️ WARN"
                            st.write(f"**Tagline:** {status}")
                            if critique_report["tagline"]["retries"] > 0:
                                st.caption(f"Retries: {critique_report['tagline']['retries']}")
                        with col_blog:
                            status = "✅ PASS" if critique_report["blog"]["pass"] else "⚠️ WARN"
                            st.write(f"**Blog:** {status}")
                            if critique_report["blog"]["retries"] > 0:
                                st.caption(f"Retries: {critique_report['blog']['retries']}")
                        with col_social:
                            status = "✅ PASS" if critique_report["social"]["pass"] else "⚠️ WARN"
                            st.write(f"**Social:** {status}")
                            if critique_report["social"]["retries"] > 0:
                                st.caption(f"Retries: {critique_report['social']['retries']}")
                        
                        if critique_report["warning"]:
                            st.warning("⚠️ Some content did not pass quality checks after 2 retries. Please review before publishing.")
        except Exception as e:
            st.warning(f"⚠️ Critic evaluation failed: {str(e)}. Proceeding with original content.")

        # Step 4: Hero Image
        status_text.info("⏳ Step 4/5: Generating hero image...")
        progress_bar.progress(0.75)
        with right_col:
            with st.spinner("🖼️ Creating hero image..."):
                hero_image_url = generate_image(
                    product_name, target_audience, brand_tone
                )
                with st.container(border=True):
                    st.markdown(
                        '<div class="section-heading">🖼️ Hero Image</div>',
                        unsafe_allow_html=True,
                    )
                    st.image(hero_image_url, use_container_width=True)

        # Step 5: Video
        status_text.info("⏳ Step 5/5: Generating promotional video...")
        progress_bar.progress(0.9)
        with right_col:
            with st.spinner("🎬 Creating video..."):
                try:
                    video_url = generate_video(hero_image_url, product_name, brand_tone)
                    with st.container(border=True):
                        st.markdown(
                            '<div class="section-heading">🎬 Promotional Video</div>',
                            unsafe_allow_html=True,
                        )
                        if video_url:
                            st.video(video_url)
                            st.caption(f"Video URL: {video_url[:80]}...")
                        else:
                            st.warning("⚠️ Video URL is empty")
                except VideoAPIError as e:
                    st.warning(f"⚠️ Video generation failed: {str(e)}")
                except Exception as e:
                    st.warning(f"⚠️ Video playback error: {type(e).__name__}: {str(e)}")

        # Step 6: Voiceover
        status_text.info("⏳ Step 6/5: Generating voiceover...")

        progress_bar.progress(0.95)
        voiceover_data = None
        with right_col:
            with st.spinner("🎙️ Creating voiceover..."):
                try:
                    voiceover_data = generate_voiceover(blog, product_name)
                    with st.container(border=True):
                        st.markdown(
                            '<div class="section-heading">🎙️ Voiceover</div>',
                            unsafe_allow_html=True,
                        )
                        st.markdown("**Narration Script:**")
                        st.write(voiceover_data["script"])
                        st.audio(voiceover_data["audio_path"])
                        with open(voiceover_data["audio_path"], "rb") as f:
                            st.download_button(
                                label="📥 Download MP3",
                                data=f.read(),
                                file_name=f"{product_name}_voiceover.mp3",
                                mime="audio/mp3",
                                key="download_voiceover_generation",
                            )
                except VoiceoverError as e:
                    st.warning(f"⚠️ Voiceover generation failed: {str(e)}")
                except Exception as e:
                    st.warning(f"⚠️ Voiceover generation crashed: {type(e).__name__}: {str(e)}")


        progress_bar.progress(1.0)
        status_text.empty()

        return {
            "tagline": tagline,
            "blog": blog,
            "social_posts": social_posts,
            "hero_image_url": hero_image_url,
            "video_url": video_url,
            "voiceover_script": voiceover_data["script"] if voiceover_data else None,
            "voiceover_path": voiceover_data["audio_path"] if voiceover_data else None,
            "report": critique_report,
        }

    except TextAPIError as e:
        progress_bar.empty()
        status_text.empty()
        st.error("❌ Text generation failed")
        st.warning(
            "**Most likely cause:** OpenRouter free daily quota exhausted.\n\n"
            "**Fix options:**\n"
            "- Wait until tomorrow (UTC midnight) for quota to reset\n"
            "- Add credits at https://openrouter.ai/settings/credits\n"
            "- Create a new API key at https://openrouter.ai/keys\n\n"
            f"Details: {e}"
        )
        return None

    except (ImageAPIError, VideoAPIError) as e:
        progress_bar.empty()
        status_text.empty()
        st.error("❌ Image/Video generation failed")
        st.info(f"Details: {e}")
        return None

    except TimeoutError as e:
        progress_bar.empty()
        status_text.empty()
        st.error(f"⏱️ Request timed out: {str(e)}")
        st.warning(
            "The API took too long to respond. Please try again in a moment."
        )
        return None

    except ValueError as e:
        progress_bar.empty()
        status_text.empty()
        st.error(f"❌ Configuration error: {str(e)}")
        st.info("Please check your .env file and ensure all API keys are valid.")
        return None

    except Exception as e:
        progress_bar.empty()
        status_text.empty()
        error_msg = str(e).lower()

        if "401" in error_msg or "unauthorized" in error_msg:
            st.error("❌ Authentication failed - check your API keys")
            st.info("Verify that all API keys in your .env file are correct.")
        elif "429" in error_msg or "rate" in error_msg:
            st.error("❌ Rate limit exceeded - please wait before trying again")
        elif "invalid" in error_msg or "malformed" in error_msg:
            st.error(f"❌ Invalid request: {str(e)}")
        else:
            st.error(f"❌ Error generating campaign: {str(e)}")
            st.info(
                "💡 Common issues:\n- Invalid API credentials\n"
                "- Network connectivity\n- Service unavailable\n\n"
                "Please try again in a moment."
            )
        return None


def render_success_section(
    product_name: str, campaign_data: Dict
) -> None:
    """Render Stage 1 success message and download button."""
    st.success("✅ Campaign generated successfully! Your marketing assets are ready to use.")

    st.markdown("---")

    download_content = format_download_content(
        product_name,
        campaign_data["tagline"],
        campaign_data["blog"],
        campaign_data["social_posts"],
        campaign_data["hero_image_url"],
        campaign_data["video_url"],
    )

    st.download_button(
        label="📥 Download Campaign Assets",
        data=download_content,
        file_name=format_filename(product_name),
        mime="text/plain",
        use_container_width=True,
    )


def render_stage2_section(
    product_name: str, campaign_data: Dict
) -> None:
    """Render Stage 2: Content Engine Pro features."""
    st.markdown("---")
    st.markdown(
        """
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                -webkit-background-clip: text; 
                -webkit-text-fill-color: transparent; 
                font-size: 2rem; font-weight: 700;">
    🚀 Content Engine Pro (Stage 2)
    </div>
    """,
        unsafe_allow_html=True,
    )
    st.markdown("Advanced features: AI Self-Critique, Voiceover, Multi-Channel Adaptation")
    st.markdown("---")

    # Critic Verdict Section
    report = campaign_data.get("report")
    if report:
        st.markdown("### 🤖 AI Self-Critique Verdict")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            status = "✅ PASS" if report["tagline"]["pass"] else "⚠️ WARN"
            st.metric("Tagline", status, f"Retries: {report['tagline']['retries']}")
            if report["tagline"]["issue"]:
                st.caption(f"Issue: {report['tagline']['issue']}")
        
        with col2:
            status = "✅ PASS" if report["blog"]["pass"] else "⚠️ WARN"
            st.metric("Blog", status, f"Retries: {report['blog']['retries']}")
            if report["blog"]["issue"]:
                st.caption(f"Issue: {report['blog']['issue']}")
        
        with col3:
            status = "✅ PASS" if report["social"]["pass"] else "⚠️ WARN"
            st.metric("Social", status, f"Retries: {report['social']['retries']}")
            if report["social"]["issue"]:
                st.caption(f"Issue: {report['social']['issue']}")
        
        if report.get("warning"):
            st.warning("⚠️ Some content did not pass quality checks after 2 retries. Please review before publishing.")
        
        st.markdown("---")
    else:
        st.info("ℹ️ Critic evaluation unavailable")
        st.markdown("---")

    # Voiceover Section
    if campaign_data.get("voiceover_script"):
        st.markdown("### 🎙️ Voiceover")
        st.markdown("**Narration Script:**")
        st.write(campaign_data["voiceover_script"])
        if campaign_data.get("voiceover_path"):
            try:
                st.audio(campaign_data["voiceover_path"])
                with open(campaign_data["voiceover_path"], "rb") as f:
                    st.download_button(
                        label="📥 Download MP3",
                        data=f.read(),
                        file_name=f"{product_name}_voiceover.mp3",
                        mime="audio/mp3",
                        key="download_voiceover_display",
                    )
            except Exception as e:
                st.warning(f"⚠️ Could not load audio file: {str(e)}")
        st.markdown("---")

    # Multi-Channel Adaptation Section
    st.markdown("### 🔄 Multi-Channel Adaptation")
    
    channel = st.selectbox(
        "Select a channel to adapt the campaign:",
        options=["B2B LinkedIn", "Gen-Z TikTok", "Parents Facebook"],
        label_visibility="collapsed",
    )

    if st.button("📝 Adapt Campaign", use_container_width=True):
        with st.spinner(f"🔄 Adapting campaign for {channel}..."):
            try:
                adapted = adapt_for_channel(
                    campaign_data["tagline"],
                    campaign_data["blog"],
                    campaign_data["social_posts"],
                    channel,
                )
                
                st.markdown("---")
                st.markdown(f"### ✨ {channel} Campaign")
                
                # Display adapted tagline
                with st.container(border=True):
                    st.markdown('<div class="section-heading">✨ Adapted Tagline</div>', unsafe_allow_html=True)
                    st.write(adapted["tagline"])
                
                # Display adapted blog
                with st.container(border=True):
                    st.markdown('<div class="section-heading">📝 Adapted Blog</div>', unsafe_allow_html=True)
                    st.write(adapted["blog"])
                
                # Display adapted social posts
                with st.container(border=True):
                    st.markdown('<div class="section-heading">📱 Adapted Social Posts</div>', unsafe_allow_html=True)
                    st.markdown("**🐦 Twitter:**")
                    st.write(adapted["social"]["twitter"])
                    st.markdown("**📷 Instagram:**")
                    st.write(adapted["social"]["instagram"])
                    st.markdown("**💼 LinkedIn:**")
                    st.write(adapted["social"]["linkedin"])
                    
            except AdaptationError as e:
                st.error(f"❌ Adaptation failed: {e}")
            except TimeoutError:
                st.error("⏱️ Adaptation request timed out. Please try again.")
            except Exception as e:
                st.error(f"❌ Error adapting campaign: {str(e)}")


def main() -> None:
    """Main application entry point."""
    render_sidebar()
    render_header()
    validate_api_keys()

    product_name, target_audience, brand_tone = render_input_section()

    if st.button("🎯 Generate Campaign", use_container_width=True, type="primary"):
        # Validate inputs
        is_valid, error_msg = validate_inputs(product_name, target_audience)
        if not is_valid:
            st.error(f"❌ {error_msg}")
            st.stop()

        # Clean inputs
        product_name = product_name.strip()
        target_audience = target_audience.strip()

        # Generate campaign
        left_col, right_col = st.columns(2, gap="large")
        campaign_data = generate_campaign(
            product_name, target_audience, brand_tone, left_col, right_col
        )

        # Display success and download option
        if campaign_data:
            render_success_section(product_name, campaign_data)
            render_stage2_section(product_name, campaign_data)


if __name__ == "__main__":
    main()
