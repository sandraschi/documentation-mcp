# AI Workflow Sampling Standards

## Overview
Standards for implementing AI workflow sampling in MCP servers, enabling true AI-guided creative and iterative processes.

## Sampling Architecture

### Core Principles
- **Iterative Refinement**: AI models sample from creative tools and refine outputs
- **Workflow Continuity**: Maintain state across sampling iterations
- **Performance Optimization**: Efficient sampling pipelines for real-time workflows
- **Error Recovery**: Graceful handling of sampling failures

### Sampling Method Requirements

#### 1. Sample Generation
```python
@app.tool()
async def sample_creative_workflow(
    ctx,
    base_design: str,
    iterations: int = 5,
    refinement_prompt: str = ""
) -> Dict[str, Any]:
    """Generate iterative samples for AI-guided creative workflows.

    Args:
        base_design: Initial design or content to sample from
        iterations: Number of sampling iterations (default: 5)
        refinement_prompt: AI instructions for sampling refinement

    Returns:
        Dict containing sampling results and workflow state
    """
    results = []
    current_state = base_design

    for i in range(iterations):
        # Generate variation based on AI prompt
        variation = await generate_variation(current_state, refinement_prompt)

        # Apply sampling transformation
        transformed = await apply_transformation(variation)

        # Capture result for AI workflow
        result = await capture_sample(transformed)
        results.append({
            "iteration": i + 1,
            "variation": variation,
            "result": result,
            "workflow_state": await get_workflow_state()
        })

        current_state = transformed

    return {
        "sampling_complete": True,
        "iterations_completed": len(results),
        "results": results,
        "final_workflow_state": await get_workflow_state(),
        "ai_workflow_enabled": True,
        "sampling_method": "iterative_refinement"
    }
```

#### 2. State Management
```python
class SamplingState:
    """Manages sampling workflow state across iterations."""

    def __init__(self):
        self.iterations = []
        self.current_state = None
        self.metadata = {}

    async def save_iteration(self, iteration_data: Dict) -> None:
        """Save iteration data for workflow continuity."""
        self.iterations.append(iteration_data)
        await self.persist_state()

    async def get_workflow_context(self) -> Dict:
        """Get context for AI decision making."""
        return {
            "iteration_count": len(self.iterations),
            "current_state": self.current_state,
            "patterns": self.analyze_patterns(),
            "recommendations": self.generate_recommendations()
        }
```

## Creative Server Sampling Patterns

### Blender MCP Sampling
```python
@app.tool()
async def sample_blender_scene(
    ctx,
    scene_description: str,
    sampling_params: Dict[str, Any]
) -> Dict[str, Any]:
    """Sample Blender scene variations for AI-guided 3D creation.

    Enables AI models to iteratively sample and refine 3D scenes
    through direct Blender integration.
    """
    # Initialize scene
    scene = await blender_init_scene(scene_description)

    # Iterative sampling
    variations = []
    for iteration in range(sampling_params.get("iterations", 3)):
        # Generate AI-guided variation
        variation = await ai_generate_scene_variation(scene, sampling_params)

        # Apply in Blender
        result_scene = await blender_apply_variation(scene, variation)

        # Render sample
        sample = await blender_render_sample(result_scene)

        variations.append({
            "iteration": iteration + 1,
            "variation": variation,
            "sample": sample,
            "scene_data": result_scene
        })

        scene = result_scene

    return {
        "sampling_type": "blender_scene",
        "variations": variations,
        "final_scene": scene,
        "ai_guidance_applied": True
    }
```

### GIMP/Inkscape Sampling
```python
@app.tool()
async def sample_graphic_design(
    ctx,
    design_concept: str,
    style_parameters: Dict[str, Any]
) -> Dict[str, Any]:
    """Sample graphic design variations for AI-guided creative workflows.

    Enables iterative design refinement through AI sampling.
    """
    # Initialize design
    design = await init_design_canvas(design_concept)

    # Style-based sampling
    samples = []
    for style in style_parameters.get("styles", ["minimal", "bold", "organic"]):
        # Generate AI-guided style application
        styled_design = await ai_apply_design_style(design, style)

        # Apply graphic transformations
        final_design = await apply_graphic_transformations(styled_design)

        # Export sample
        sample_data = await export_design_sample(final_design)

        samples.append({
            "style": style,
            "design": final_design,
            "sample": sample_data,
            "ai_enhancements": True
        })

    return {
        "sampling_type": "graphic_design",
        "concept": design_concept,
        "samples": samples,
        "design_workflow": "ai_guided"
    }
```

## Performance Optimization

### Sampling Efficiency Patterns
```python
class SamplingOptimizer:
    """Optimizes sampling performance for real-time AI workflows."""

    def __init__(self):
        self.cache = {}
        self.batch_size = 5
        self.concurrency_limit = 3

    async def optimize_sampling_pipeline(self, samples: List[Dict]) -> List[Dict]:
        """Optimize sampling pipeline for performance."""
        # Batch processing
        batches = [samples[i:i + self.batch_size]
                  for i in range(0, len(samples), self.batch_size)]

        optimized_results = []
        semaphore = asyncio.Semaphore(self.concurrency_limit)

        async def process_batch(batch):
            async with semaphore:
                return await self.process_batch_concurrent(batch)

        # Concurrent batch processing
        tasks = [process_batch(batch) for batch in batches]
        batch_results = await asyncio.gather(*tasks)

        for batch_result in batch_results:
            optimized_results.extend(batch_result)

        return optimized_results
```

### Caching Strategies
```python
class SamplingCache:
    """Cache sampling results to improve performance."""

    def __init__(self, ttl_seconds: int = 3600):
        self.cache = {}
        self.ttl = ttl_seconds

    async def get_cached_sample(self, key: str) -> Optional[Dict]:
        """Retrieve cached sampling result if still valid."""
        if key in self.cache:
            cached = self.cache[key]
            if time.time() - cached["timestamp"] < self.ttl:
                return cached["result"]
            else:
                del self.cache[key]
        return None

    async def cache_sample(self, key: str, result: Dict) -> None:
        """Cache sampling result with timestamp."""
        self.cache[key] = {
            "result": result,
            "timestamp": time.time()
        }
```

## Error Handling and Recovery

### Sampling Failure Recovery
```python
@app.tool()
async def recover_sampling_failure(
    ctx,
    failed_iteration: int,
    error_details: Dict[str, Any]
) -> Dict[str, Any]:
    """Recover from sampling pipeline failures.

    Implements intelligent recovery strategies for AI workflow continuity.
    """
    recovery_strategies = [
        "retry_with_reduced_complexity",
        "fallback_to_cached_result",
        "generate_alternative_approach",
        "rollback_to_previous_iteration"
    ]

    # Analyze failure
    failure_analysis = await analyze_sampling_failure(error_details)

    # Select recovery strategy
    strategy = await select_recovery_strategy(failure_analysis)

    # Execute recovery
    recovery_result = await execute_recovery(strategy, failed_iteration)

    return {
        "recovery_applied": True,
        "strategy_used": strategy,
        "recovered_iteration": failed_iteration,
        "recovery_result": recovery_result,
        "workflow_continuity": "maintained"
    }
```

## Quality Metrics

### Sampling Quality Assessment
```python
def assess_sampling_quality(samples: List[Dict]) -> Dict[str, float]:
    """Assess quality metrics for sampling results."""
    return {
        "diversity_score": calculate_diversity(samples),
        "innovation_score": calculate_innovation(samples),
        "coherence_score": calculate_coherence(samples),
        "ai_guidance_effectiveness": calculate_ai_effectiveness(samples)
    }
```

## Integration with AI Workflows

### AI-Guided Sampling Prompts
```python
SAMPLING_PROMPTS = {
    "creative_exploration": """
    Generate creative variations that explore different design directions.
    Focus on innovation while maintaining coherence with the original concept.
    Provide diverse options for the user to choose from.
    """,

    "iterative_refinement": """
    Refine the current design based on previous iterations.
    Build upon successful elements while introducing subtle improvements.
    Maintain consistency with established design language.
    """,

    "problem_solving": """
    Address specific design challenges through targeted sampling.
    Focus on functional improvements and user experience enhancements.
    Generate solutions that solve identified problems.
    """
}
```

## Testing Sampling Implementations

### Sampling Unit Tests
```python
@pytest.mark.asyncio
async def test_sampling_workflow():
    """Test complete sampling workflow."""
    # Setup
    initial_state = {"design": "basic_concept"}

    # Execute sampling
    result = await sample_creative_workflow(
        iterations=3,
        refinement_prompt="Make it more modern"
    )

    # Assertions
    assert result["sampling_complete"] is True
    assert len(result["results"]) == 3
    assert result["ai_workflow_enabled"] is True
    assert "final_workflow_state" in result

@pytest.mark.asyncio
async def test_sampling_error_recovery():
    """Test sampling error recovery mechanisms."""
    # Simulate failure scenario
    failed_result = await sample_with_simulated_failure()

    # Verify recovery
    assert "recovery_applied" in failed_result
    assert failed_result["workflow_continuity"] == "maintained"
```

## Next Steps
After implementing sampling, consider:
1. [Performance Monitoring](./performance-monitoring.md)
2. [AI Integration Standards](./ai-integration.md)
3. [Workflow Orchestration](./workflow-orchestration.md)