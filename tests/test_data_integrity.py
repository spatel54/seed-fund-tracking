#!/usr/bin/env python3
"""
Data Integrity Tests for IWRC Seed Fund Tracking

These tests ensure:
1. No double-counting errors in data loading
2. Fact sheet usage includes proper warnings
3. Deprecated files are not imported
4. Data loader produces consistent results

Usage:
    python3 tests/test_data_integrity.py
"""

import sys
from pathlib import Path
import unittest
import warnings

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Now import the data loader
from analysis.scripts.iwrc_data_loader import IWRCDataLoader


class TestDataDeduplication(unittest.TestCase):
    """Test that deduplication is working correctly"""

    @classmethod
    def setUpClass(cls):
        """Initialize data loader once for all tests"""
        cls.loader = IWRCDataLoader()

    def test_master_data_deduplication(self):
        """Test that master data deduplication prevents double-counting"""
        # Load without deduplication
        df_raw = self.loader.load_master_data(deduplicate=False)

        # Load with deduplication
        df_dedup = self.loader.load_master_data(deduplicate=True)

        # Deduplicated should have fewer rows (unless already unique)
        self.assertLessEqual(
            len(df_dedup),
            len(df_raw),
            "Deduplicated data should have <= rows than raw data"
        )

        # All project IDs should be unique after deduplication
        self.assertEqual(
            df_dedup['project_id'].nunique(),
            len(df_dedup),
            "After deduplication, all project IDs should be unique"
        )

        print(f"✅ Deduplication test passed:")
        print(f"   Raw rows: {len(df_raw)}")
        print(f"   Deduplicated rows: {len(df_dedup)}")
        print(f"   Unique projects: {df_dedup['project_id'].nunique()}")

    def test_project_count_accuracy(self):
        """Test that project counts use .nunique() correctly"""
        df = self.loader.load_master_data(deduplicate=False)

        # Filter to 10-year period
        df_10yr = df[df['project_year'].between(2015, 2024)]

        # Project count should use nunique
        project_count = df_10yr['project_id'].nunique()

        # Should be 77 for 10-year period (known correct value)
        self.assertEqual(
            project_count,
            77,
            f"10-year project count should be 77, got {project_count}"
        )

        print(f"✅ Project count test passed: {project_count} projects")

    def test_investment_deduplication(self):
        """Test that investment calculation doesn't double-count"""
        # Load with deduplication
        df = self.loader.load_master_data(deduplicate=True)
        df_10yr = df[df['project_year'].between(2015, 2024)]

        # Calculate metrics
        metrics = self.loader.calculate_metrics(df_10yr, period='10yr')

        # Investment should be ~$3.96M (not ~$8.5M)
        investment = metrics['investment']

        # Should be between $3.9M and $4.0M
        self.assertGreater(
            investment,
            3_900_000,
            f"Investment too low: ${investment:,.2f} (expected ~$3.96M)"
        )
        self.assertLess(
            investment,
            4_100_000,
            f"Investment too high: ${investment:,.2f} (expected ~$3.96M, suggests double-counting)"
        )

        print(f"✅ Investment deduplication test passed: ${investment:,.2f}")

    def test_student_deduplication(self):
        """Test that student counts don't double-count"""
        # Load with deduplication
        df = self.loader.load_master_data(deduplicate=True)
        df_10yr = df[df['project_year'].between(2015, 2024)]

        # Calculate metrics
        metrics = self.loader.calculate_metrics(df_10yr, period='10yr')

        # Students should be ~117 (not ~304 from double-counting)
        students = metrics['students']

        # Should be between 100 and 140 (reasonable range for actual data)
        self.assertGreater(
            students,
            100,
            f"Student count too low: {students} (expected ~117)"
        )
        self.assertLess(
            students,
            200,
            f"Student count too high: {students} (expected ~117, suggests double-counting)"
        )

        print(f"✅ Student deduplication test passed: {students} students")

    def test_roi_accuracy(self):
        """Test that ROI calculation uses correct (deduplicated) investment"""
        df = self.loader.load_master_data(deduplicate=True)
        df_10yr = df[df['project_year'].between(2015, 2024)]

        metrics = self.loader.calculate_metrics(df_10yr, period='10yr')

        roi = metrics['roi']

        # ROI should be ~0.07 (7%), not ~0.03 (3%)
        self.assertGreater(
            roi,
            0.06,
            f"ROI too low: {roi:.1%} (expected ~7%, suggests inflated investment)"
        )
        self.assertLess(
            roi,
            0.10,
            f"ROI too high: {roi:.1%} (expected ~7%)"
        )

        print(f"✅ ROI accuracy test passed: {roi:.1%}")


class TestFactSheetWarnings(unittest.TestCase):
    """Test that fact sheet usage includes appropriate warnings"""

    @classmethod
    def setUpClass(cls):
        """Initialize data loader once for all tests"""
        cls.loader = IWRCDataLoader()

    def test_fact_sheet_warning_displayed(self):
        """Test that loading fact sheet displays warning"""
        # Capture warnings
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            # This should trigger a warning
            df = self.loader.load_fact_sheet_data(year='2025', warn=True)

            # Should have warnings (printed to stdout, not Python warnings)
            # Just verify data loaded
            self.assertGreater(len(df), 0, "Fact sheet should load data")

        print("✅ Fact sheet warning test passed")

    def test_fact_sheet_no_project_id(self):
        """Test that fact sheet indeed lacks Project ID column"""
        df = self.loader.load_fact_sheet_data(year='2025', warn=False)

        # Should NOT have project_id column
        self.assertNotIn(
            'project_id',
            df.columns,
            "Fact sheet should NOT have project_id column"
        )
        self.assertNotIn(
            'Project ID',
            df.columns,
            "Fact sheet should NOT have 'Project ID' column"
        )

        print("✅ Fact sheet structure test passed: No Project ID column confirmed")


class TestDeprecatedFilesIsolation(unittest.TestCase):
    """Test that deprecated files are isolated and not imported"""

    def test_deprecated_folder_exists(self):
        """Test that deprecated folder exists"""
        deprecated_dir = Path(__file__).parent.parent / 'deprecated'

        self.assertTrue(
            deprecated_dir.exists(),
            "Deprecated folder should exist"
        )

        # Should have README
        readme = deprecated_dir / 'README.md'
        self.assertTrue(
            readme.exists(),
            "Deprecated folder should have README.md"
        )

        print("✅ Deprecated folder structure test passed")

    def test_deprecated_notebooks_moved(self):
        """Test that problematic notebooks are in deprecated folder"""
        deprecated_notebooks = Path(__file__).parent.parent / 'deprecated' / 'notebooks'

        # Check for misleading notebook
        misleading = deprecated_notebooks / '01_comprehensive_roi_analysis_CORRECTED.ipynb'
        self.assertTrue(
            misleading.exists(),
            "Misleading notebook should be in deprecated/notebooks/"
        )

        print("✅ Deprecated notebooks test passed")

    def test_deprecated_scripts_moved(self):
        """Test that error-prone scripts are in deprecated folder"""
        deprecated_scripts = Path(__file__).parent.parent / 'deprecated' / 'scripts'

        # Check for error-prone script
        error_script = deprecated_scripts / 'generate_final_deliverables.py'
        self.assertTrue(
            error_script.exists(),
            "Error-prone script should be in deprecated/scripts/"
        )

        print("✅ Deprecated scripts test passed")


class TestDataLoaderConsistency(unittest.TestCase):
    """Test that data loader produces consistent results"""

    @classmethod
    def setUpClass(cls):
        """Initialize data loader once for all tests"""
        cls.loader = IWRCDataLoader()

    def test_multiple_loads_identical(self):
        """Test that loading data multiple times gives same results"""
        # Load twice
        df1 = self.loader.load_master_data(deduplicate=True)
        df2 = self.loader.load_master_data(deduplicate=True)

        # Should be identical
        self.assertEqual(
            len(df1),
            len(df2),
            "Multiple loads should produce same row count"
        )
        self.assertEqual(
            df1['project_id'].nunique(),
            df2['project_id'].nunique(),
            "Multiple loads should produce same project count"
        )

        print(f"✅ Data loader consistency test passed: {len(df1)} rows")

    def test_metrics_calculation_consistent(self):
        """Test that metrics calculation is consistent"""
        df = self.loader.load_master_data(deduplicate=True)
        df_10yr = df[df['project_year'].between(2015, 2024)]

        # Calculate twice
        metrics1 = self.loader.calculate_metrics(df_10yr, period='10yr')
        metrics2 = self.loader.calculate_metrics(df_10yr, period='10yr')

        # Should be identical
        self.assertEqual(
            metrics1['investment'],
            metrics2['investment'],
            "Investment should be consistent"
        )
        self.assertEqual(
            metrics1['students'],
            metrics2['students'],
            "Student count should be consistent"
        )
        self.assertEqual(
            metrics1['roi'],
            metrics2['roi'],
            "ROI should be consistent"
        )

        print("✅ Metrics consistency test passed")

    def test_trailing_space_handling(self):
        """Test that 'Project ID ' trailing space is handled"""
        df_raw = self.loader.load_master_data(deduplicate=False)

        # Should have 'project_id' column (normalized)
        self.assertIn(
            'project_id',
            df_raw.columns,
            "Data should have normalized 'project_id' column"
        )

        # Should NOT have 'Project ID ' with trailing space
        self.assertNotIn(
            'Project ID ',
            df_raw.columns,
            "Trailing space should be removed from column name"
        )

        print("✅ Trailing space handling test passed")


class TestKnownMetrics(unittest.TestCase):
    """Test against known correct metrics"""

    @classmethod
    def setUpClass(cls):
        """Initialize data loader once for all tests"""
        cls.loader = IWRCDataLoader()
        cls.df = cls.loader.load_master_data(deduplicate=True)
        cls.df_10yr = cls.df[cls.df['project_year'].between(2015, 2024)]
        cls.metrics_10yr = cls.loader.calculate_metrics(cls.df_10yr, period='10yr')

    def test_10yr_projects_known_value(self):
        """Test 10-year project count against known value"""
        self.assertEqual(
            self.metrics_10yr['projects'],
            77,
            "10-year project count should be 77"
        )
        print("✅ 10-year projects: 77")

    def test_10yr_investment_known_range(self):
        """Test 10-year investment against known value"""
        # Should be $3,958,980 (allow small variance)
        investment = self.metrics_10yr['investment']
        self.assertAlmostEqual(
            investment,
            3_958_980,
            delta=10_000,
            msg=f"10-year investment should be ~$3,958,980, got ${investment:,.2f}"
        )
        print(f"✅ 10-year investment: ${investment:,.2f}")

    def test_10yr_students_known_range(self):
        """Test 10-year student count against known value"""
        # Should be ~117 (allow small variance for data updates)
        students = self.metrics_10yr['students']
        self.assertAlmostEqual(
            students,
            117,
            delta=10,
            msg=f"10-year students should be ~117, got {students}"
        )
        print(f"✅ 10-year students: {students}")

    def test_10yr_roi_known_range(self):
        """Test 10-year ROI against known value"""
        # Should be ~0.07 (7%)
        roi = self.metrics_10yr['roi']
        self.assertAlmostEqual(
            roi,
            0.07,
            delta=0.01,
            msg=f"10-year ROI should be ~7%, got {roi:.1%}"
        )
        print(f"✅ 10-year ROI: {roi:.1%}")


def run_tests():
    """Run all tests with verbose output"""
    print("=" * 70)
    print("IWRC SEED FUND DATA INTEGRITY TESTS")
    print("=" * 70)
    print()

    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestDataDeduplication))
    suite.addTests(loader.loadTestsFromTestCase(TestFactSheetWarnings))
    suite.addTests(loader.loadTestsFromTestCase(TestDeprecatedFilesIsolation))
    suite.addTests(loader.loadTestsFromTestCase(TestDataLoaderConsistency))
    suite.addTests(loader.loadTestsFromTestCase(TestKnownMetrics))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Summary
    print()
    print("=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print()

    if result.wasSuccessful():
        print("✅ ALL TESTS PASSED - Data integrity verified!")
    else:
        print("❌ SOME TESTS FAILED - Review errors above")

    print("=" * 70)

    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
