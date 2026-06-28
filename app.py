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
    from config import OPENROUTER_API_KEY, REPLICATE_API_KEY
except Exception as _cfg_error:
    st.error(f"❌ Configuration error: {_cfg_error}")
    st.stop()

from text_gen import generate_tagline, generate_blog_intro, generate_social_posts, TextAPIError
from image_gen import generate_image, MediaAPIError as ImageAPIError
from video_gen import generate_video, MediaAPIError as VideoAPIError
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
    if not REPLICATE_API_KEY:
        errors.append("❌ **REPLICATE_API_KEY** is missing — required for video generation (get free token at replicate.com)")

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
                video_url = generate_video(hero_image_url, product_name, brand_tone)
                with st.container(border=True):
                    st.markdown(
                        '<div class="section-heading">🎬 Promotional Video</div>',
                        unsafe_allow_html=True,
                    )
                    st.video(video_url)

        progress_bar.progress(1.0)
        status_text.empty()

        return {
            "tagline": tagline,
            "blog": blog,
            "social_posts": social_posts,
            "hero_image_url": hero_image_url,
            "video_url": video_url,
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
    """Render success message and download button."""
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


if __name__ == "__main__":
    main()
