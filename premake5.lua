workspace("Popart_Graphs")
	configurations({"debug", "release"})


	project("popart_graphs")
		kind("ConsoleApp")
		language("C++")
		cppdialect("C++17")

		includedirs({
			"include",
			"popart/src/tree",
		})
		files({
			--"src/*.cpp",
			"popart/src/testgraphs.cpp"
		})

		location("build")
		--targetdir("build/bin/${cfg.buildcfg}")
		--targetname("popart_graphs")
		filter({})
		links({
			"popart"
		})
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
