workspace("Popart_Networks")
	configurations({"debug", "release"})

	newoption({
		trigger = "kind",
		category = "Custom",
		description = "Kind of binary when building",
		default = "shared",
		allowed = {
			{"exe", "Executable"},
			{"static", "Static library"},
			{"shared", "Shared library"},
		}
	})
	newoption({
		trigger = "nopython",
		category = "Custom",
		description = "Disable Python bindings"
	})
	newoption({
		trigger = "pythonversion",
		category = "Custom",
		description = "Python version to link against for non-Windows systems",
		default = "3.11"
	})

	project("popart_networks")
		filter("options:kind=exe")
			kind("ConsoleApp")
		filter("options:kind=static")
			kind("StaticLib")
		filter("options:kind=shared")
			kind("SharedLib")
		filter("options:*")
		language("C++")
		cppdialect("C++17")

		includedirs({
			"include",
			"popart/src",
		})
		filter({"system:not windows"})
			includedirs("/usr/include/python" .. _OPTIONS["pythonversion"])
		filter({})
		files({
			"src/*.cpp",
			--"popart/src/testgraphs.cpp"
		})
		filter({"not options:nopython", "system:windows"})
			removefiles({
				"src/python_wrapper.cpp",
			})
		filter({})

		location("build")
		--targetdir("build/bin/${cfg.buildcfg}")
		--targetname("popart_networks")
		filter({})
		links({
			"popart"
		})
		filter({"not options:nopython", "system:windows"})
			links("python3")
		filter({"not options:nopython", "system:not windows"})
			links("python" .. _OPTIONS["pythonVersion"])
		filter({})
		--pic("On")
		linkoptions({})
		warnings("Extra")
		filter({"not system:windows"})
			buildoptions({"-pedantic"})
			disablewarnings({
				"unused-parameter",
				"comment",
				"catch-value",
				"sign-compare"
			})

		filter({"configurations:debug"})
			defines({"DEBUG"})
			optimize("Debug")
			symbols("On")

		filter({"configurations:release"})
			defines({"NDEBUG"})
			optimize("Full")
			--symbols("Off")


	project("popart")
		kind("SharedLib")
		language("C++")
		cppdialect("C++17")

		includedirs({
			"popart/src/networks",
			"popart/src/tree",
			"popart/src/seqio",
		})
		files({
			"popart/src/networks/*.cpp",
			"popart/src/tree/*.cpp",
			"popart/src/seqio/*.cpp",
		})

		location("build")
		filter({})
		links({"lpsolve55"})
		--pic("On")
		linkoptions({})
		warnings("Extra")
		filter({"not system:windows"})
			--buildoptions({"-pedantic"})
			disablewarnings({
				"unused-parameter",
				"sign-compare",
				"deprecated-copy",
				"mismatched-new-delete",
				"maybe-uninitialized",
				"char-subscripts",
				"misleading-indentation",
				"implicit-fallthrough",
				"unused-but-set-variable",
				"unused-result",
			})

		filter({"configurations:debug"})
			defines({"DEBUG"})
			optimize("Debug")
			symbols("On")

		filter({"configurations:release"})
			defines({"NDEBUG"})
			optimize("Full")
			--symbols("Off")
